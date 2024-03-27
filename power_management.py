import time
import psutil

# Constants
BATTERY_THRESHOLD = 45 # Battery percentage threshold below which to activate power-saving
SLEEP_TIME = 10  # Time in seconds for processes to sleep
PROCESS_IGNORE_LIST = ["explorer.exe", "system", "python", "chrome.exe", "firefox.exe", "code.exe"]  # Processes to keep active

def get_battery_usage():
    battery = psutil.sensors_battery()
    if battery is not None:
        percent = battery.percent
        power_plugged = battery.power_plugged
        if power_plugged:
            status = "Charging"
        else:
            status = "Discharging"

        return percent, status
    else:
        return None, None
    

def sleep_background_processes():
    battery_percent, battery_status = get_battery_usage()
    for process in psutil.process_iter(attrs=["pid", "name"]):
        try:
            process_name = process.info["name"]
            process_pid = process.info["pid"]
            
            if process_name not in PROCESS_IGNORE_LIST:
                if battery_percent < BATTERY_THRESHOLD:
                    print(f"Sleeping background process: {process_name} (PID: {process_pid})")
                    psutil.Process(process_pid).suspend()
                    time.sleep(SLEEP_TIME)
                    psutil.Process(process_pid).resume()
                    print(f"Sleeping process resumed")
                else:
                    print(f"No process is sleeping")
                    print(f"Current Battery Percentage: {battery_percent}%")
                    print(f"Current Battery Status: {battery_status}")
                    break
            
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def main():
    print("Monitoring battery usage in real-time...")
    print("Power Management Tool - Reducing Battery Consumption")
    try:
        while True:
            #battery_percent, battery_status = get_battery_usage()
            #if battery_percent is not None:
            #   print(f"Battery: {battery_percent}% | Status: {battery_status}")
            #else:
            #   print("Battery information not available.")

            
            battery = psutil.sensors_battery()
            if battery is not None:
                battery_percent, battery_status = get_battery_usage()
                if battery_percent <= BATTERY_THRESHOLD and battery_status == "Discharging":
                    print(f"Low battery ({battery_percent})%") 
                    print(f"Current Battery Status ({battery_status}) ")
                    print(f"Initiating power-saving measures.")
                    sleep_decision = input("Do you want to put background processes to sleep? (y/n): ")
                    if sleep_decision.lower() == "y":
                        print(f"Putting background processes to sleep")
                        sleep_background_processes()
                    else:
                        print(f"No process is sleeping")
                        break
                else:
                    print(f"Battery: {battery_percent}% ")
                    print(f"Battery Status: {battery_status} ")
                    print(f"Normal operation, No background processes are sleeping")
                    sleep_decision = input("Do you want to put background processes to sleep? (y/n): ")
                    if sleep_decision.lower() == "y":
                        print(f"Putting background processes to sleep")
                        sleep_background_processes()
                    else:
                        print(f"No process is sleeping")
                        break
            else:
                print("Battery information not available.")
            
            time.sleep(60)  # Adjust the interval as desired
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")
        print("Power management tool stopped by user.")

if __name__ == "__main__":
    main()