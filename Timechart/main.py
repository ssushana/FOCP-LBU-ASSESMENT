import sys
from pathlib import Path
from timing_board import TimingBoard

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py <lap_file>")
        return

    timing_file = sys.argv[1]
    board = TimingBoard()
    
    driver_details_file = "f1_drivers.txt"
    if Path(driver_details_file).exists():
        board.load_driver_details(driver_details_file)

    if board.process_timing_file(timing_file):
        board.display_results()

if __name__ == "__main__":
    main()
