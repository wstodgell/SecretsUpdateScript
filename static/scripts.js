// Creates and submits a form to save configuration for a given section.
// Gathers input fields from the specified section, builds a hidden form, and sends a POST request
// to "/save_config" with the collected data.
function saveConfig(section) {
  console.log(`Saving configuration for section: ${section}`);

  const form = document.createElement("form");
  form.method = "POST";
  form.action = "/save_config";

  //creates a new HTML <input> element in JavaScript.
  const sectionInput = document.createElement("input");
  sectionInput.type = "hidden";
  sectionInput.name = "section";
  sectionInput.value = section;
  form.appendChild(sectionInput);

  // Add profile selection input
  const profileSelect = document.getElementById("profile_select");
  const profileInput = document.createElement("input");
  profileInput.type = "hidden";
  profileInput.name = "profile_select"; // Match the key used in the backend
  profileInput.value = profileSelect.value; // Get the selected value
  form.appendChild(profileInput);

  //selects all <input> elements within a form or container that has a class matching the section variable.
  //This allows targeting a specific group of input fields, like those in the AWS or GitHub configuration sections.
  const fields = document.querySelectorAll(`.${section} input`);
  fields.forEach((field) => {
    const input = document.createElement("input");
    input.type = "hidden";
    input.name = field.name;
    input.value = field.value;
    form.appendChild(input);
    console.log(`Added hidden input: ${field.name} = ${field.value}`);
  });
  // append this new form to the DOM
  document.body.appendChild(form);
  // programmatically triggers the submission of the form. In this case it is form.action = "/save_config";
  form.submit();
}

// Called when index.HTML file has a file changed - event has a target (from file HTML object)
// Handles file upload, reads the file content, and triggers parsing.
// Uses FileReader to read the selected file as text and passes the content
// to parseFileContent() for further processing.
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

// Function to parse the content of a file, assumed to be in INI-like format
// 1. Splits the file content into individual lines for processing.
// 2. Initializes an empty `profiles` object to store profiles and `currentProfile` to track the active profile.
// 3. Iterates through each line of the file:
//    a. If a line starts and ends with square brackets, it indicates a new profile section.
//       - The profile name is extracted by removing the brackets, and a new empty object is created for that profile.
//    b. If the line contains an '=' sign (key-value pair), the key and value are extracted and trimmed of whitespace.
//       - The key-value pair is stored within the current profile's object in the `profiles` dictionary.
// 4. This results in a `profiles` object where each profile is a key, and the associated key-value pairs are stored as an object under each profile.
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

// Populates the dropdown (profile_select - in index.html) with profile names and updates the form fields based on the selected profile.
// and event listener is added so that corresponding fields can be updated when new options is selected.
function populateProfileDropdown(profiles) {
  console.log("Populating profile dropdown");
  // retrieves the profile_select control from index.html
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

function populateFieldsFromProfile() {
  // Get the selected profile from the dropdown
  const profileSelect = document.getElementById("profile_select");
  const selectedProfile = profileSelect.value;

  // Assuming `profiles` is the object containing all the profiles
  if (profiles[selectedProfile]) {
    // Update the fields with the selected profile's data
    document.getElementById("aws_access_key_id").value =
      profiles[selectedProfile].aws_access_key_id || "";
    document.getElementById("aws_secret_access_key").value =
      profiles[selectedProfile].aws_secret_access_key || "";
  }
}
