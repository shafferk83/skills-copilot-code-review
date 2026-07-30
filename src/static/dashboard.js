document.addEventListener("DOMContentLoaded", () => {
  // DOM elements
  const lookupSection = document.getElementById("lookup-section");
  const dashboardSection = document.getElementById("dashboard-section");
  const studentEmailInput = document.getElementById("student-email");
  const lookupButton = document.getElementById("lookup-button");
  const lookupMessage = document.getElementById("lookup-message");
  const studentLogoutButton = document.getElementById("student-logout-button");
  const cardActivities = document.getElementById("card-activities");

  // Profile elements
  const profileName = document.getElementById("profile-name");
  const profileEmail = document.getElementById("profile-email");
  const profileGrade = document.getElementById("profile-grade");
  const profileBranch = document.getElementById("profile-branch");
  const enrolledActivitiesList = document.getElementById("enrolled-activities-list");

  // Current student state
  let currentStudent = null;

  // Check if a student session is saved
  function checkSavedSession() {
    const saved = localStorage.getItem("currentStudent");
    if (saved) {
      try {
        currentStudent = JSON.parse(saved);
        showDashboard(currentStudent);
      } catch (e) {
        localStorage.removeItem("currentStudent");
      }
    }
  }

  // Fetch student profile from the API
  async function fetchStudentProfile(email) {
    showLookupMessage("Looking up your profile…", "info");
    try {
      const response = await fetch(
        `/students/${encodeURIComponent(email)}`
      );

      if (response.status === 404) {
        showLookupMessage("No student found with that email address.", "error");
        return;
      }

      if (!response.ok) {
        showLookupMessage("An error occurred. Please try again.", "error");
        return;
      }

      const data = await response.json();
      currentStudent = data;
      localStorage.setItem("currentStudent", JSON.stringify(data));
      hideLookupMessage();
      showDashboard(data);
    } catch (error) {
      console.error("Error fetching student profile:", error);
      showLookupMessage("Failed to connect to the server. Please try again.", "error");
    }
  }

  // Show dashboard with student data
  function showDashboard(student) {
    profileName.textContent = student.name;
    profileEmail.textContent = student.email;
    profileGrade.textContent = `Grade ${student.grade}`;
    profileBranch.textContent = student.branch;

    renderEnrolledActivities(student.enrolled_activities || []);

    lookupSection.classList.add("hidden");
    dashboardSection.classList.remove("hidden");
  }

  // Render enrolled activities list
  function renderEnrolledActivities(activities) {
    if (activities.length === 0) {
      enrolledActivitiesList.innerHTML =
        '<p class="no-results">You are not enrolled in any activities yet.</p>';
      return;
    }

    enrolledActivitiesList.innerHTML = activities
      .map(
        (name) => `
      <div class="enrolled-activity-item">
        <span class="enrolled-activity-icon">🏅</span>
        <span class="enrolled-activity-name">${escapeHtml(name)}</span>
      </div>`
      )
      .join("");
  }

  // Escape HTML to prevent XSS
  function escapeHtml(text) {
    const div = document.createElement("div");
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
  }

  // Show a message in the lookup section
  function showLookupMessage(text, type) {
    lookupMessage.textContent = text;
    lookupMessage.className = `message ${type}`;
    lookupMessage.classList.remove("hidden");
  }

  // Hide the lookup message
  function hideLookupMessage() {
    lookupMessage.classList.add("hidden");
  }

  // Logout – clear session and return to lookup view
  function studentLogout() {
    currentStudent = null;
    localStorage.removeItem("currentStudent");
    studentEmailInput.value = "";
    hideLookupMessage();
    dashboardSection.classList.add("hidden");
    lookupSection.classList.remove("hidden");
  }

  // Event listeners
  lookupButton.addEventListener("click", () => {
    const email = studentEmailInput.value.trim();
    if (!email) {
      showLookupMessage("Please enter your email address.", "error");
      return;
    }
    fetchStudentProfile(email);
  });

  studentEmailInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      lookupButton.click();
    }
  });

  studentLogoutButton.addEventListener("click", studentLogout);

  // Activities quick-access card navigates back to main page
  cardActivities.addEventListener("click", () => {
    window.location.href = "/static/index.html";
  });

  // Initialize – restore session if available
  checkSavedSession();
});
