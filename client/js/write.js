const UNSPLASH_ACCESS_KEY = '-wt55k5MvE8RrFEweKVIQzLWuOMsysfXYRQXJGBhjOs';
let BASE_URL = `http://127.0.0.1:8000/`;


const editor = new MediumEditor('.editable', {
    toolbar: false 
});

// Toggle custom toolbar based on text selection
document.addEventListener('selectionchange', () => {
    const toolbar = document.getElementById('editor-toolbar');
    const selection = window.getSelection();

    if (selection.rangeCount > 0 && !selection.isCollapsed) {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();

        toolbar.style.display = 'block';
        toolbar.style.top = `${rect.top + window.scrollY - toolbar.offsetHeight - 10}px`;
        toolbar.style.left = `${rect.left + window.scrollX}px`;
    } else {
        toolbar.style.display = 'none';
    }
});

function formatText(command, value = null) {
    document.execCommand(command, false, value);
}

// Toolbar button event listeners
document.querySelector('.bold-btn').addEventListener('click', () => formatText('bold'));
document.querySelector('.italic-btn').addEventListener('click', () => formatText('italic'));
document.querySelector('.h1-btn').addEventListener('click', () => formatText('formatBlock', 'H1'));
document.querySelector('.h2-btn').addEventListener('click', () => formatText('formatBlock', 'H2'));
document.querySelector('.quote-btn').addEventListener('click', () => formatText('formatBlock', 'BLOCKQUOTE'));

// Search for images on Unsplash
async function searchUnsplash() {
    const query = document.getElementById('imageSearch').value.trim();
    if (!query) return;

    const url = `https://api.unsplash.com/search/photos?query=${query}&client_id=${UNSPLASH_ACCESS_KEY}`;

    try {
        const response = await fetch(url);
        const data = await response.json();
        displayImages(data.results);
    } catch (error) {
        console.error("Error fetching images:", error);
    }
}

let selectedFile = null; // Variable to store the currently selected file

// Trigger file input for image upload
function triggerFileInput() {
    document.getElementById('imageUpload').click();
}

// Display the uploaded image
function displayUploadedImg(event) {
    const file = event.target.files[0];
    if (file) {
        const imgURL = URL.createObjectURL(file);
        displayImages([{ urls: { regular: imgURL } }]);
        selectedFile = file;
    }
}


// Display images in the result container
function displayImages(images) {
    const imageResults = document.getElementById('imageResults');
    imageResults.innerHTML = '';
    images.forEach(image => {
        const imgElement = document.createElement('img');
        imgElement.src = image.urls.regular;
        imgElement.onclick = () => selectImage(imgElement)
        imageResults.appendChild(imgElement);
    });
   
}

function selectImage(imgElement){
    const imageResults = document.getElementById('imageResults')
    imageResults.innerHTML = '';
    imageResults.appendChild(imgElement.cloneNode())
    const imageUrl = imgElement.src;

    //Fetch the image and convert it to a blob
    fetch(imageUrl)
        .then((response)=>{
            if (!response.ok) {
                throw new Error(`Failed to fetch image. Status: ${response.status}`)
            }
            return response.blob();
        })
        .then((blob)=>{
            const fileName = `unsplash-${Date.now()}.jpg`;
            selectedFile = new File([blob], fileName, { type: blob.type });
        })
        .catch((error)=>{
            console.error("Error Creating Blob:", error);
        })
}

// Upload the selected image
// async function uploadImage() {
//     console.log(selectedFile)
//     if (!selectedFile) {
//         alert("No image selected!");
//         return;
//     }

//     const formData = new FormData();
//     formData.append("file", selectedFile);
//     // console.log(formData)

//     try {
//         const uploadResponse = await fetch(`${BASE_URL}upload-image`, {
//             method: "POST",
//             body: formData,
//         });

//         if (uploadResponse.ok) {
//             const result = await uploadResponse.json();
//             console.log("Image uploaded successfully:", result);
//         } else {
//             console.error("Error uploading image. Status:", uploadResponse.status);
//         }
//     } catch (error) {
//         console.error("Request failed:", error);
//     }
// }




//function to publice the blog
async function submitPost() {
    console.log("from SubmitPost",selectedFile)
    if (!selectedFile) {
        alert("Image upload failed. Please try again or upload from your system.");
        triggerFileInput();
        return;
    }

    const formData = new FormData();
    formData.append("file", selectedFile);
    let uploadedFilename=null;

    try {
        const uploadResponse = await fetch(`${BASE_URL}posts/upload-image`, {
            method: "POST",
            body: formData,
        });

        if (uploadResponse.ok) {
            const result = await uploadResponse.json();
            uploadedFilename = result.filename
        } else {
            console.error("Error uploading image. Status:", uploadResponse.status);
            return;
        }
    } catch (error) {
        console.error("Request failed:", error);
        return;
    }
    
    if (!uploadedFilename) {
        alert("Image upload failed. Please try again.")
        return;
    }


    const token = localStorage.getItem("accessToken");
    const postTitle = document.querySelector("#title-input").value;
    const postSummary = document.querySelector("#summary-input").value;
    const postContent = document.querySelector("#editor-data").innerText;

    try {
        const response = await fetch(`${BASE_URL}posts`, {
            method: "POST",
            body: JSON.stringify({
                title: postTitle,
                summary: postSummary,
                content: postContent,
                image_post: uploadedFilename, // Include the uploaded image filename
                published: true,
            }),
            headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
            },
        });

        if (response.ok) {
            const postres = await response.json();
        } else {
            console.error("Error creating post. Status:", response.status);
        }
    } catch (error) {
        console.error("Request failed:", error);
    }
}

// const imageResults1=document.querySelector('#imageResults img');
// console.log(imageResults1.src);
// async function uploadImage(blob) {
//     const formData = new FormData();
//     formData.append('image', blob, 'uploaded-image.jpg');

//     const response = await fetch(`${BASE_URL}upload-image`,{
//         method: 'POSST',
//         body: formData,
//     });

//     if (response.ok) {
//         console.log("Image uploaded successfully!");
//     }else{
//         console.error('Failed to upload image')
//     }
// }

// function publicePost()



// // Function to search for images on Unsplash
// async function searchUnsplash() {
//     const query = document.getElementById('imageSearch').value.trim();
//     if (!query) return;
  
//     const url = `https://api.unsplash.com/search/photos?query=${query}&client_id=${UNSPLASH_ACCESS_KEY}`;
  
//     try {
//       const response = await fetch(url);
//       const data = await response.json();
//       displayImages(data.results);
//     } catch (error) {
//       console.error("Error fetching images:", error);
//     }
//   }
  
//   // Function to display images from Unsplash search results
//   function displayImages(images) {
//     const imageResults = document.getElementById('imageResults');
//     imageResults.innerHTML = '';
  
//     images.forEach(image => {
//       const img = document.createElement('img');
//       img.src = image.urls.thumb;
//       img.alt = image.alt_description;
//       img.onclick = () => selectImage(img);
//       imageResults.appendChild(img);
//     });
//   }
  
//   // Function to handle image selection
//   function selectImage(img) {
//     const imageResults = document.getElementById('imageResults');
//     imageResults.innerHTML = ''; // Clear all images
//     imageResults.appendChild(img.cloneNode()); // Keep only the selected image
//   }
  
//   // Trigger the hidden file input when the button is clicked
//   function triggerFileInput() {
//       document.getElementById('imageUpload').click();
//     }
    
//     // Display the uploaded image
//     function displayUploadedImg(event) {
//       const imageResults = document.getElementById('imageResults');
//       imageResults.innerHTML = ''; // Clear previous images
    
//       const file = event.target.files[0];
//       if (file && file.type.startsWith('image/')) {
//         const img = document.createElement('img');
//         img.src = URL.createObjectURL(file);
//         img.alt = 'Uploaded image';
//         img.onload = () => URL.revokeObjectURL(img.src); // Release memory
//         imageResults.appendChild(img);
//       }
//     }