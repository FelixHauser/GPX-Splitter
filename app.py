import sys
import xml.etree.ElementTree as ET
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

def split_gpx(file_path, delete_waypoints):
    tree = ET.parse(file_path)
    root = tree.getroot()
    namespace = {'gpx': 'http://www.topografix.com/GPX/1/1'}  # GPX namespace
    
    waypoints = root.findall(".//gpx:wpt", namespace)
    
    if delete_waypoints:
        # Create a new GPX file for the waypoints
        waypoints_gpx = ET.Element(root.tag, root.attrib)
        for waypoint in waypoints:
            waypoints_gpx.append(waypoint)
        
        waypoints_tree = ET.ElementTree(waypoints_gpx)
        waypoints_output_file = Path(file_path).parent / f"{Path(file_path).stem}_waypoints.gpx"
        waypoints_tree.write(waypoints_output_file, encoding="utf-8", xml_declaration=True)
        print(f"Saved waypoints to: {waypoints_output_file}")

        # Remove waypoints from the original GPX file
        for waypoint in waypoints:
            root.remove(waypoint)
            print("Removed a waypoint.")
    
    # Find all track segments
    tracks = root.findall(".//gpx:trk", namespace)
    output_dir = Path(file_path).parent / f"{Path(file_path).stem}_segments"
    output_dir.mkdir(exist_ok=True)
    
    for track in tracks:
        name_elem = track.find("gpx:name", namespace)
        segment_name = name_elem.text if name_elem is not None else "Unnamed"
        
        new_gpx = ET.Element(root.tag, root.attrib)
        new_gpx.append(track)
        new_tree = ET.ElementTree(new_gpx)
        output_file = output_dir / f"{segment_name}.gpx"
        
        new_tree.write(output_file, encoding="utf-8", xml_declaration=True)
        print(f"Saved segment: {output_file}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Open file dialog to select GPX file
    file_path = filedialog.askopenfilename(title="Select a GPX file", filetypes=[("GPX files", "*.gpx")])
    
    if not file_path:
        print("No file selected. Exiting.")
        sys.exit(1)

    # Ask user whether they want to delete waypoints
    delete_waypoints = messagebox.askyesno(
        "Delete Waypoints",
        "Do you want to delete the waypoints (points of interest) in the GPX file?"
    )

    # Call the split function with the user's choice
    split_gpx(file_path, delete_waypoints)


 # pyinstaller --onefile --windowed --name GPX_Splitter app.py