let BASE_URL = `http://127.0.0.1:8000/`;


const searchForm = document.querySelector('form');
const searchInput = document.querySelector('.form-input');
const articlesContainer = document.querySelector('#posts-container-search'); 
// console.log(articlesContainer)

// Fetch all posts on page load or when no search query is provided
async function fetchAllPosts() {
    try {
        const response = await fetch(`${BASE_URL}posts`);
        if (!response.ok) {
            throw new Error(`Error fetching posts: ${response.status}`);
        }
        
        const data = await response.json();
        console.log(data)
        displaySearchResults(data);
    } catch (error) {
        console.error('Error fetching all posts:', error);
    }
}

// Adding an event listener to the form for search
searchForm.addEventListener('submit', async (event) => {
    event.preventDefault(); 
    const query = searchInput.value.trim();


    if (!query) {
        console.log("No search query provided, fetching all posts.");
        fetchAllPosts();
        return;
    }

    // Fetch filtered data from the backend
    try {
        const response = await fetch(`${BASE_URL}posts?search=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error(`Error fetching posts: ${response.status}`);
        }

        const data = await response.json();
        displaySearchResults(data); 
    } catch (error) {
        console.error('Search error:', error);
    }
});

// Function to display search results or the default blog list
function displaySearchResults(posts) {
    articlesContainer.innerHTML = "";
  
    posts.forEach((postData) => {
      const post = postData.PostRead;
      const likes = postData.likes;
      const noComment = postData.noComment;
  
      console.log(post);
  
      const postHTML = `
          <div class="home-article">
              <div class="home-article-content">
                  <span id="author">${post.user.username}</span>
                  <a href="/blog.html?id=${post.id}"
                      ><h2>${post.title}</h2>
                      <h3>${post.summary}</h3>
                  </a>
                  <a href="/blog.html?id=${post.id}">
                      <div class="meta">
                          <span>${new Date(post.created_at).toLocaleDateString('en-US',{ year:'numeric',month:'short', day:'numeric'})}</span>
                          <div class="likes">
                              <img src="svg/like.svg" alt="" srcset="" />
                              <button class="n"><span>${likes}</span></button>
                          </div>
                          <div class="comments">
                              <button class="ind-commBtn" aria-label="responses">
                                  <img src="svg/comment.svg" alt="" srcset="" />
                              </button>
                              <button class="n">${noComment}<span></span></button>
                          </div>
                      </div>
                  </a>
              </div>
              <div class="home-article-img">
                  <img src="img/shubham-dhage.jpg" alt="article" />
              </div>
          </div>
          `;
  
          articlesContainer.innerHTML += postHTML;
    });
  }
fetchAllPosts()