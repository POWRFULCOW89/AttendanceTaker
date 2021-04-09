from attendance import AttendanceTaker

# Constraints

base_url = "https://avalid.moodleplatform.com.uk"
AT = AttendanceTaker(base_url)

##############################################

# Login
AT.loadCredentials("credentials.json")
AT.login()

# Look up course
print(AT.currentPage())
AT.navigateToCourseById(2481) # Embedded in the url: "https://avalid.moodleplatform.com.uk/course/view.php?id=1111"

# Take attendance
print(AT.currentPage())
AT.takeAttendance()        

# Logout
AT.logout()

print(AT.currentPage())
AT.exit()

print("Attendance has been taken. Please verify.")
