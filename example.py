from attendance import AttendanceTaker

# Constraints

base_url = "https://avalid.moodleplatform.com.uk/course/view.php?id=1111"
AT = AttendanceTaker(base_url)

##############################################

try:
    # Login
    AT.loadCredentials("credentials.json")
    AT.login()

    # Look up course
    AT.navigateToCourseById(2481) # Embedded in the url: "https://avalid.moodleplatform.com.uk/course/view.php?id=1111"

    # Take attendance
    AT.takeAttendance()        

    print("Attendance has been taken. Please verify.")

    # Logout
    AT.logout()

finally:
    # Clean up afterwards
    AT.exit()
    