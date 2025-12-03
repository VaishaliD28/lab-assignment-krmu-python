import os
import logging
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
print("Matplotlib working!")


# =========================
# Logging Setup (Task 5)
# =========================
logging.basicConfig(
    filename="energy.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


# =========================
# Task 1: Data Ingestion & Validation
# =========================

def load_all_building_data(data_dir: Path) -> pd.DataFrame:
    """
    Reads all .csv files from data/ folder and merges into single DataFrame.
    Expected at least these columns in each file: timestamp, kwh
    If building name/month not present, we add from filename.
    """
    all_frames = []

    if not data_dir.exists():
        logging.error(f"Data directory not found: {data_dir}")
        print("Data folder nahi mila. 'data' naam ka folder bana aur CSV daal.")
        return pd.DataFrame()

    for csv_file in data_dir.glob("*.csv"):
        logging.info(f"Reading file: {csv_file.name}")
        try:
            # on_bad_lines='skip' to avoid corrupt rows
            df = pd.read_csv(csv_file, on_bad_lines='skip')

            # Basic check
            if 'timestamp' not in df.columns or 'kwh' not in df.columns:
                logging.warning(f"File {csv_file.name} missing required columns.")
                continue

            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            df = df.dropna(subset=['timestamp'])

            # Add metadata if not present
            if 'building' not in df.columns:
                # building name from filename before first '_', or full stem
                building_name = csv_file.stem.split("_")[0]
                df['building'] = building_name

            if 'month' not in df.columns:
                df['month'] = df['timestamp'].dt.month

            all_frames.append(df)

        except FileNotFoundError:
            logging.error(f"File not found: {csv_file}")
        except Exception as e:
            logging.error(f"Error reading {csv_file}: {e}")

    if not all_frames:
        logging.warning("No valid CSV files found.")
        return pd.DataFrame()

    df_combined = pd.concat(all_frames, ignore_index=True)
    logging.info(f"Combined DataFrame shape: {df_combined.shape}")
    return df_combined


# =========================
# Task 2: Core Aggregation Logic
# =========================

def calculate_daily_totals(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.set_index('timestamp')
    daily = df.resample('D')['kwh'].sum().reset_index()
    daily.rename(columns={'kwh': 'daily_kwh'}, inplace=True)
    return daily


def calculate_weekly_aggregates(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.set_index('timestamp')
    weekly = df.resample('W')['kwh'].sum().reset_index()
    weekly.rename(columns={'kwh': 'weekly_kwh'}, inplace=True)
    return weekly


def building_wise_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary = (
        df.groupby('building')['kwh']
        .agg(['mean', 'min', 'max', 'sum'])
        .reset_index()
        .rename(columns={'sum': 'total'})
    )
    return summary


# =========================
# Task 3: Object-Oriented Modeling
# =========================

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


class Building:
    def __init__(self, name):
        self.name = name
        self.meter_readings = []

    def add_reading(self, reading: MeterReading):
        self.meter_readings.append(reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.meter_readings)

    def generate_report(self):
        if not self.meter_readings:
            return {
                "building": self.name,
                "total_kwh": 0,
                "num_readings": 0,
            }
        total = self.calculate_total_consumption()
        num = len(self.meter_readings)
        return {
            "building": self.name,
            "total_kwh": total,
            "num_readings": num,
        }


class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def get_or_create_building(self, name: str) -> Building:
        if name not in self.buildings:
            self.buildings[name] = Building(name)
        return self.buildings[name]

    def load_from_dataframe(self, df: pd.DataFrame):
        for _, row in df.iterrows():
            bname = row['building']
            building = self.get_or_create_building(bname)
            reading = MeterReading(row['timestamp'], row['kwh'])
            building.add_reading(reading)

    def generate_all_reports(self):
        reports = []
        for b in self.buildings.values():
            reports.append(b.generate_report())
        return pd.DataFrame(reports)


# =========================
# Task 4: Visual Output with Matplotlib
# =========================

def create_dashboard_plot(df: pd.DataFrame, daily: pd.DataFrame,
                          weekly: pd.DataFrame, output_path: Path):
    if df.empty:
        print("Data empty hai, plot nahi banega.")
        return

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    # 1) Trend Line – daily consumption over time for all buildings
    axs[0].plot(daily['timestamp'], daily['daily_kwh'])
    axs[0].set_title("Daily Total Consumption")
    axs[0].set_xlabel("Date")
    axs[0].set_ylabel("kWh")

    # 2) Bar Chart – compare average weekly usage across buildings
    # For simplicity: building-wise mean of weekly consumption
    df_weekly_building = (
        df.copy()
        .set_index('timestamp')
        .groupby('building')['kwh']
        .resample('W')
        .sum()
        .reset_index()
    )
    weekly_mean_by_building = df_weekly_building.groupby('building')['kwh'].mean()
    axs[1].bar(weekly_mean_by_building.index, weekly_mean_by_building.values)
    axs[1].set_title("Average Weekly Usage per Building")
    axs[1].set_xlabel("Building")
    axs[1].set_ylabel("kWh")
    axs[1].tick_params(axis='x', rotation=45)

    # 3) Scatter Plot – peak-hour consumption vs time/building
    # Simple version: scatter of timestamps vs kwh, color-coded by building index
    df_sorted = df.sort_values('kwh', ascending=False).head(200)  # top points only
    building_codes = {b: i for i, b in enumerate(df_sorted['building'].unique())}
    colors = df_sorted['building'].map(building_codes)

    axs[2].scatter(df_sorted['timestamp'], df_sorted['kwh'], c=colors)
    axs[2].set_title("Peak Consumption Points")
    axs[2].set_xlabel("Time")
    axs[2].set_ylabel("kWh")

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)
    logging.info(f"Dashboard saved to {output_path}")


# =========================
# Task 5: Persistence & Executive Summary
# =========================

def save_outputs(df_combined: pd.DataFrame,
                 building_summary: pd.DataFrame,
                 daily: pd.DataFrame,
                 weekly: pd.DataFrame):
    # Cleaned dataset
    cleaned_path = OUTPUT_DIR / "cleaned_energy_data.csv"
    df_combined.to_csv(cleaned_path, index=False)

    # Building summary
    summary_path = OUTPUT_DIR / "building_summary.csv"
    building_summary.to_csv(summary_path, index=False)

    # Summary text
    summary_txt_path = OUTPUT_DIR / "summary.txt"

    total_campus = df_combined['kwh'].sum()

    # Highest-consuming building
    highest_building = building_summary.sort_values('total', ascending=False).iloc[0]

    # Peak load time
    peak_row = df_combined.loc[df_combined['kwh'].idxmax()]

    with summary_txt_path.open("w", encoding="utf-8") as f:
        f.write("Energy Usage Executive Summary\n")
        f.write("===============================\n\n")
        f.write(f"Total campus consumption: {total_campus:.2f} kWh\n")
        f.write(
            f"Highest-consuming building: {highest_building['building']} "
            f"({highest_building['total']:.2f} kWh)\n"
        )
        f.write(
            f"Peak load time: {peak_row['timestamp']} "
            f"({peak_row['kwh']:.2f} kWh)\n\n"
        )
        f.write("Daily trend: see cleaned_energy_data.csv and dashboard.png\n")
        f.write("Weekly trend: see building_summary.csv and dashboard.png\n")

    logging.info("Outputs (CSV + summary.txt) saved.")


# =========================
# MAIN SCRIPT (sab tasks chain me)
# =========================

def main():
    print("Energy Analytics Script Running...")

    # Task 1: Load & validate
    df_combined = load_all_building_data(DATA_DIR)

    if df_combined.empty:
        print("Koi valid data nahi mila. Script stop ho gayi.")
        return

    # Make sure types are correct
    df_combined['timestamp'] = pd.to_datetime(df_combined['timestamp'])
    df_combined['kwh'] = pd.to_numeric(df_combined['kwh'], errors='coerce')
    df_combined = df_combined.dropna(subset=['kwh'])

    # Task 2: Aggregations
    daily = calculate_daily_totals(df_combined)
    weekly = calculate_weekly_aggregates(df_combined)
    building_summary_df = building_wise_summary(df_combined)

    # Task 3: OOP modeling
    manager = BuildingManager()
    manager.load_from_dataframe(df_combined)
    reports_df = manager.generate_all_reports()

    # Optionally print building OOP reports
    print("\nBuilding Reports (OOP Based):")
    print(reports_df)

    # Task 4: Dashboard plot
    dashboard_path = OUTPUT_DIR / "dashboard.png"
    create_dashboard_plot(df_combined, daily, weekly, dashboard_path)

    # Task 5: Save outputs + summary
    save_outputs(df_combined, building_summary_df, daily, weekly)

    print("\nDone! CSV files + summary + dashboard.png saved in 'output' folder.")


if __name__ == "__main__":
    main()
