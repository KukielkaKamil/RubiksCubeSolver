import cv2
import numpy as np

def nothing(x):
    pass

def create_calibration_gui():
    # Create a window
    cv2.namedWindow("Calibration")

    # Create trackbars for lower and upper HSV ranges
    cv2.createTrackbar("Low H", "Calibration", 0, 179, nothing)
    cv2.createTrackbar("High H", "Calibration", 179, 179, nothing)
    cv2.createTrackbar("Low S", "Calibration", 0, 255, nothing)
    cv2.createTrackbar("High S", "Calibration", 255, 255, nothing)
    cv2.createTrackbar("Low V", "Calibration", 0, 255, nothing)
    cv2.createTrackbar("High V", "Calibration", 255, 255, nothing)

def get_trackbar_values():
    # Get values from trackbars
    low_h = cv2.getTrackbarPos("Low H", "Calibration")
    high_h = cv2.getTrackbarPos("High H", "Calibration")
    low_s = cv2.getTrackbarPos("Low S", "Calibration")
    high_s = cv2.getTrackbarPos("High S", "Calibration")
    low_v = cv2.getTrackbarPos("Low V", "Calibration")
    high_v = cv2.getTrackbarPos("High V", "Calibration")
    return (low_h, low_s, low_v), (high_h, high_s, high_v)

def main():
    # Open the camera
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Camera not accessible")
        return

    create_calibration_gui()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Convert to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Get current HSV ranges from trackbars
        lower, upper = get_trackbar_values()
        lower = np.array(lower, dtype=np.uint8)
        upper = np.array(upper, dtype=np.uint8)

        # Create a mask based on HSV ranges
        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # Show the original and result side by side
        combined = np.hstack((frame, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), result))
        cv2.imshow("Calibration", combined)

        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Print the final HSV ranges
    print("Final HSV Ranges:")
    print(f"Lower: {lower}")
    print(f"Upper: {upper}")

    # Release resources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
