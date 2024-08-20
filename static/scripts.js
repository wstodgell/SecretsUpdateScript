function saveConfig(section) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/save_config';

    const sectionInput = document.createElement('input');
    sectionInput.type = 'hidden';
    sectionInput.name = 'section';
    sectionInput.value = section;
    form.appendChild(sectionInput);

    const fields = document.querySelectorAll(`.${section} input`);
    fields.forEach(field => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = field.name;
        input.value = field.value;
        form.appendChild(input);
    });

    document.body.appendChild(form);
    form.submit();
}

function anotherFunction() {
    alert("Another button clicked!");
    // Add your additional functionality here
}

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(e) {
            parseFileContent(e.target.result);
        };
        reader.readAsText(file);
    }
}


//Extracts key-value pairs from file content and updates form fields accordingly. 
//Specifically targets 'aws_access_key_id' and 'aws_secret_access_key'.
function parseFileContent(content) {
    const lines = content.split('\n');
    let awsAccessKeyId = '';
    let awsSecretAccessKey = '';

    lines.forEach(line => {
        if (line.startsWith('aws_access_key_id')) {
            awsAccessKeyId = line.split('=')[1].trim();
        } else if (line.startsWith('aws_secret_access_key')) {
            awsSecretAccessKey = line.split('=')[1].trim();
        }
    });

    if (awsAccessKeyId && awsSecretAccessKey) {
        document.getElementById('aws_access_key_id').value = awsAccessKeyId;
        document.getElementById('aws_secret_access_key').value = awsSecretAccessKey;
    }
}
