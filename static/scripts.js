function saveConfig(section) {
  console.log(`Saving configuration for section: ${section}`);

  const form = document.createElement("form");
  form.method = "POST";
  form.action = "/save_config";

  const sectionInput = document.createElement("input");
  sectionInput.type = "hidden";
  sectionInput.name = "section";
  sectionInput.value = section;
  form.appendChild(sectionInput);

  const fields = document.querySelectorAll(`.${section} input`);
  fields.forEach((field) => {
    const input = document.createElement("input");
    input.type = "hidden";
    input.name = field.name;
    input.value = field.value;
    form.appendChild(input);
    console.log(`Added hidden input: ${field.name} = ${field.value}`);
  });

  document.body.appendChild(form);
  form.submit();
}

function anotherFunction() {
  console.log("Another button clicked!");
  alert("Another button clicked!");
  // Add your additional functionality here
}

function handleFileUpload(event) {
  console.log("Handling file upload");
  const file = event.target.files[0];
  if (file) {
    console.log(`File selected: ${file.name}`);
    const reader = new FileReader();
    reader.onload = function (e) {
      console.log("File loaded");
      parseFileContent(e.target.result);
    };
    reader.readAsText(file);
  } else {
    console.log("No file selected");
  }
}

function parseFileContent(content) {
  console.log("Parsing file content");
  const lines = content.split("\n");
  let profiles = {};
  let currentProfile = "";

  lines.forEach((line) => {
    line = line.trim();
    if (line.startsWith("[") && line.endsWith("]")) {
      currentProfile = line.slice(1, -1).trim();
      profiles[currentProfile] = {};
    } else if (currentProfile && line.includes("=")) {
      const [key, value] = line.split("=").map((part) => part.trim());
      if (key && value) {
        profiles[currentProfile][key] = value;
      }
    }
  });

  console.log("Profiles found:", profiles);
  populateProfileDropdown(profiles);
}

function populateProfileDropdown(profiles) {
  console.log("Populating profile dropdown");
  const profileSelect = document.getElementById("profile_select");
  profileSelect.innerHTML = ""; // Clear existing options

  Object.keys(profiles).forEach((profile) => {
    const option = document.createElement("option");
    option.value = profile;
    option.textContent = profile;
    profileSelect.appendChild(option);
  });

  if (Object.keys(profiles).length > 0) {
    profileSelect.value = Object.keys(profiles)[0]; // Set the first profile as selected
    updateFields(profiles[profileSelect.value]);
  } else {
    console.log("No profiles available");
  }

  // Add event listener for profile selection change
  profileSelect.addEventListener("change", function () {
    const selectedProfile = profileSelect.value;
    console.log(`Profile selected: ${selectedProfile}`);
    updateFields(profiles[selectedProfile]);
  });
}

function updateFields(profile) {
  console.log("Updating fields with profile:", profile);
  if (profile.aws_access_key_id) {
    document.getElementById("aws_access_key_id").value =
      profile.aws_access_key_id;
  }
  if (profile.aws_secret_access_key) {
    document.getElementById("aws_secret_access_key").value =
      profile.aws_secret_access_key;
  }
}
