let BASE_URL = `http://127.0.0.1:8000/`;
const postsContainer = document.getElementById("posts-container");

// Fetch posts and display them
async function getPosts() {
  try {
    let response = await fetch(`${BASE_URL}posts/`);
    if (response.ok) {
      let posts = await response.json();
      displayPosts(posts);
    } else {
      console.error("Error fetching posts:", response.status);
    }
  } catch (error) {
    console.error("Error:", error);
  }
}

// Display posts on the UI
function displayPosts(posts) {
  postsContainer.innerHTML = "";

  posts.forEach((postData) => {
    const post = postData.PostRead;
    const likes = postData.likes;
    const noComment = postData.noComment;

    // Build the post HTML
    const postHTML = `
        <div class="home-article">
            <div class="home-article-content">
                <span id="author">${post.user.username}</span>
                <a href="/blog.html?id=${post.id}">
                    <h2>${post.title}</h2>
                    <h3>${post.summary}</h3>
                </a>
                <a href="/blog.html?id=${post.id}">
                    <div class="meta">
                        <span>${new Date(post.created_at).toLocaleDateString(
                          "en-US",
                          { year: "numeric", month: "short", day: "numeric" }
                        )}</span>
                        <div class="likes">
                            <img src="svg/like.svg" alt="" />
                            <button class="n"><span>${likes}</span></button>
                        </div>
                        <div class="comments">
                            <button class="ind-commBtn" aria-label="responses">
                                <img src="svg/comment.svg" alt="" />
                            </button>
                            <button class="n">${noComment}<span></span></button>
                        </div>
                    </div>
                </a>
            </div>
            <div class="home-article-img">
                <img id="post-img-${post.id}" src="img/shubham-dhage.jpg" alt="Default Image" />
            </div>
        </div>
    `;

    postsContainer.innerHTML += postHTML;

    // Fetch the image dynamically and update the img element
    if (post.image_post) {
      const imgElement = document.getElementById(`post-img-${post.id}`);
      fetchImageAndUpdate(post.image_post, imgElement);
    }
  });
}

// Fetch image from API and set it to the provided img element
async function fetchImageAndUpdate(filename, imgElement) {
  try {
    let response = await fetch(`${BASE_URL}posts/display/${filename}`);
    if (response.ok) {
      const imgBlob = await response.blob();
      const imgUrl = URL.createObjectURL(imgBlob);
      imgElement.src = imgUrl; 
      imgElement.alt = "Post Image";
    } else {
      console.error("Error fetching image:", response.status);
    }
  } catch (error) {
    console.error("Error fetching image:", error.message);
  }
}

// Initial call to fetch and render posts
getPosts();