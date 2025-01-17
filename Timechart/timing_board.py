from statistics import mean
from typing import Dict, List, Tuple

class Driver:
    def __init__(self, code: str):
        self.code = code
        self.lap_times: List[float] = []
        self.fastest_lap = float('inf')
        self.name = ""
        self.team = ""
        self.number = ""

class TimingBoard:
    def __init__(self):
        self.location = ""
        self.drivers: Dict[str, Driver] = {}
        self.driver_details: Dict[str, Dict[str, str]] = {}

    def load_driver_details(self, filename: str) -> None:
        """Load driver details from the provided file."""
        try:
            with open(filename, 'r') as f:
                for line in f:
                    number, code, name, team = line.strip().split(',')
                    self.driver_details[code] = {
                        'number': number,
                        'name': name,
                        'team': team
                    }
        except FileNotFoundError:
            print(f"Warning: Driver details file {filename} not found.")
        except Exception as e:
            print(f"Warning: Error reading driver details: {e}")

    def process_timing_file(self, filename: str) -> bool:
        """Process the timing data file."""
        try:
            with open(filename, 'r') as f:
                self.location = f.readline().strip()
                
                for line in f:
                    line = line.strip()
                    if len(line) < 4:  # Ensure the line is valid
                        continue
                    
                    driver_code = line[:3]
                    try:
                        lap_time = float(line[3:])
                    except ValueError:
                        print(f"Warning: Invalid lap time format for {driver_code}")
                        continue

                    if driver_code not in self.drivers:
                        self.drivers[driver_code] = Driver(driver_code)
                        if driver_code in self.driver_details:
                            details = self.driver_details[driver_code]
                            self.drivers[driver_code].name = details['name']
                            self.drivers[driver_code].team = details['team']
                            self.drivers[driver_code].number = details['number']
                    
                    driver = self.drivers[driver_code]
                    driver.lap_times.append(lap_time)
                    driver.fastest_lap = min(driver.fastest_lap, lap_time)
                
                return True
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
            return False
        except Exception as e:
            print(f"Error processing file: {e}")
            return False

    def get_fastest_driver(self) -> Tuple[str, float]:
        """Get the driver with the fastest lap."""
        if not self.drivers:
            return ("", float('inf'))
        
        fastest_driver = min(self.drivers.items(), key=lambda x: x[1].fastest_lap)
        return (fastest_driver[0], fastest_driver[1].fastest_lap)

    def display_results(self):
        """Display the results on the console."""
        print(f"\nFormula 1 Grand Prix - {self.location}")
        print("=" * 50)

        if not self.drivers:
            print("No timing data available.")
            return

        fastest_code, fastest_time = self.get_fastest_driver()
        fastest_driver = self.drivers[fastest_code]
        print(f"Fastest Lap: {fastest_driver.name or fastest_code} - {fastest_time:.3f}")

        all_times = [time for driver in self.drivers.values() for time in driver.lap_times]
        overall_average = mean(all_times)
        print(f"Overall Average: {overall_average:.3f}")

        print("\nDetailed Results:")
        print(f"{'Driver':<15}{'Team':<20}{'Best Lap':<10}{'Avg Lap':<10}{'Laps':<5}")
        print("=" * 50)
        for code, driver in sorted(self.drivers.items(), key=lambda x: x[1].fastest_lap):
            avg_time = mean(driver.lap_times)
            print(f"{driver.name or code:<15}{driver.team or 'N/A':<20}{driver.fastest_lap:<10.3f}{avg_time:<10.3f}{len(driver.lap_times):<5}")
