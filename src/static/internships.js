document.addEventListener("DOMContentLoaded", () => {
  const internshipsList = document.getElementById("internships-list");
  const branchFiltersContainer = document.getElementById("branch-filters");
  const searchInput = document.getElementById("internship-search");
  const searchButton = document.getElementById("search-button");

  let allInternships = [];
  let currentBranch = "";
  let searchQuery = "";

  // Branch badge colors
  const branchColors = {
    Technology:   { bg: "#e8eaf6", text: "#3949ab" },
    Science:      { bg: "#e8f5e9", text: "#2e7d32" },
    Arts:         { bg: "#f3e5f5", text: "#7b1fa2" },
    Business:     { bg: "#fff3e0", text: "#e65100" },
    Engineering:  { bg: "#fce4ec", text: "#c62828" },
    Health:       { bg: "#e0f7fa", text: "#00695c" },
    Education:    { bg: "#fffde7", text: "#f57f17" },
    "Social Studies": { bg: "#f1f8e9", text: "#558b2f" },
  };

  function getBranchStyle(branch) {
    const style = branchColors[branch];
    if (style) return `background:${style.bg};color:${style.text};`;
    return "background:#f5f5f5;color:#333;";
  }

  // Fetch available branches and populate filter buttons
  async function fetchBranches() {
    try {
      const response = await fetch("/internships/branches");
      if (!response.ok) throw new Error("Failed to fetch branches");
      const branches = await response.json();

      branches.forEach((branch) => {
        const btn = document.createElement("button");
        btn.className = "branch-filter";
        btn.dataset.branch = branch;
        btn.textContent = branch;
        branchFiltersContainer.appendChild(btn);
      });

      // Attach event listeners to all branch filter buttons
      document.querySelectorAll(".branch-filter").forEach((btn) => {
        btn.addEventListener("click", () => {
          setBranchFilter(btn.dataset.branch);
        });
      });
    } catch (error) {
      console.error("Error fetching branches:", error);
    }
  }

  function setBranchFilter(branch) {
    currentBranch = branch;
    document.querySelectorAll(".branch-filter").forEach((btn) => {
      btn.classList.toggle("active", btn.dataset.branch === branch);
    });
    renderInternships();
  }

  // Fetch all internships from the API
  async function fetchInternships() {
    internshipsList.innerHTML = "<p>Loading internships...</p>";
    try {
      const response = await fetch("/internships");
      if (!response.ok) throw new Error("Failed to fetch internships");
      allInternships = await response.json();
      renderInternships();
    } catch (error) {
      console.error("Error fetching internships:", error);
      internshipsList.innerHTML =
        '<p class="no-results">Failed to load internships. Please try again later.</p>';
    }
  }

  // Filter and render internship cards
  function renderInternships() {
    const query = searchQuery.toLowerCase();

    const filtered = allInternships.filter((internship) => {
      const matchesBranch =
        !currentBranch || internship.branch === currentBranch;
      const matchesSearch =
        !query ||
        internship.company.toLowerCase().includes(query) ||
        internship.role.toLowerCase().includes(query) ||
        internship.location.toLowerCase().includes(query) ||
        internship.branch.toLowerCase().includes(query) ||
        (internship.prerequisites || "").toLowerCase().includes(query);
      return matchesBranch && matchesSearch;
    });

    if (filtered.length === 0) {
      internshipsList.innerHTML =
        '<p class="no-results">No internships found matching your criteria.</p>';
      return;
    }

    internshipsList.innerHTML = filtered
      .map(
        (internship) => `
      <div class="internship-card">
        <span class="activity-tag internship-branch-tag" style="${getBranchStyle(internship.branch)}">${internship.branch}</span>
        <h4>${escapeHtml(internship.company)}</h4>
        <p class="internship-role">💼 ${escapeHtml(internship.role)}</p>
        <p class="internship-location">📍 ${escapeHtml(internship.location)}</p>
        ${
          internship.prerequisites
            ? `<p class="internship-prereqs"><strong>Prerequisites:</strong> ${escapeHtml(internship.prerequisites)}</p>`
            : ""
        }
        <div class="activity-card-actions">
          <a href="${escapeHtml(internship.link)}" target="_blank" rel="noopener noreferrer" class="register-button internship-link-button">
            Learn More &rarr;
          </a>
        </div>
      </div>
    `
      )
      .join("");
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.appendChild(document.createTextNode(str));
    return div.innerHTML;
  }

  // Search event listeners
  searchButton.addEventListener("click", () => {
    searchQuery = searchInput.value.trim();
    renderInternships();
  });

  searchInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      searchQuery = searchInput.value.trim();
      renderInternships();
    }
  });

  searchInput.addEventListener("input", () => {
    searchQuery = searchInput.value.trim();
    renderInternships();
  });

  // Initialize
  fetchBranches();
  fetchInternships();
});
