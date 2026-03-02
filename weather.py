import requests
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from datetime import datetime

API_KEY = "fc6e6c56cbb564bcf77cae879a206be7"  # Replace with your OpenWeather API key

def get_weather_data(cities):
    weather_data = []
    for city in cities:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url).json()
        
        if response.get("cod") != 200:
            print(f"Error fetching {city}: {response.get('message')}")
            continue
            
        weather_data.append({
            "city": city.title(),
            "temp": response["main"]["temp"],
            "humidity": response["main"]["humidity"],
            "wind": response["wind"]["speed"],
            "conditions": response["weather"][0]["description"].title(),
            "pressure": response["main"]["pressure"]
        })
    return weather_data

def create_3d_weather_chart(weather_data):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Prepare data
    cities = [data["city"] for data in weather_data]
    metrics = ["Temperature", "Humidity", "Wind", "Pressure"]
    
    # Color mapping
    colors = plt.cm.viridis(np.linspace(0, 1, len(metrics)))
    
    # Plot each metric
    for i, metric in enumerate(metrics):
        values = []
        for data in weather_data:
            if metric == "Temperature":
                values.append(data["temp"])
            elif metric == "Humidity":
                values.append(data["humidity"])
            elif metric == "Wind":
                values.append(data["wind"])
            elif metric == "Pressure":
                values.append(data["pressure"]/100)  # Normalize pressure
        
        ax.bar3d(range(len(cities)), 
                [i]*len(cities), 
                [0]*len(cities),
                dx=0.3, dy=0.3, dz=values,
                color=colors[i], alpha=0.8,
                edgecolor='white', linewidth=0.5)
    
    # Customize axes
    ax.set_xticks(range(len(cities)))
    ax.set_xticklabels(cities, rotation=45)
    ax.set_yticks(range(len(metrics)))
    ax.set_yticklabels(metrics)
    ax.set_zlabel('Values')
    
    ax.set_title('3D Weather Metrics Comparison', pad=20)
    plt.tight_layout()
    
    # Add legend
    patches = [plt.Rectangle((0,0),1,1, fc=colors[i]) 
               for i in range(len(metrics))]
    ax.legend(patches, metrics, loc='upper right')
    
    plt.savefig('weather_chart.png')
    plt.show()

def main():
    print("=== Weather Tracker with 3D Graph ===")
    cities = input("Enter cities (comma-separated): ").split(",")
    cities = [city.strip() for city in cities if city.strip()]
    
    weather_data = get_weather_data(cities)
    
    if weather_data:
        print("\nCurrent Weather Data:")
        print(f"{'City':<15} | {'Temp (°C)':<10} | {'Humidity (%)':<12} | {'Wind (m/s)':<10} | {'Pressure':<8} | Conditions")
        print("-"*80)
        for data in weather_data:
            print(f"{data['city']:<15} | {data['temp']:<10.1f} | {data['humidity']:<12} | {data['wind']:<10.1f} | {data['pressure']:<8} | {data['conditions']}")
        
        create_3d_weather_chart(weather_data)
    else:
        print("No valid weather data found")

if __name__ == "__main__":
    main()
