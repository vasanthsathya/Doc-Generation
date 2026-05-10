// Custom JavaScript for pydata-sphinx-theme

// Fetch GitHub repository data and update icon links with counts
document.addEventListener('DOMContentLoaded', function() {
  const headerInner = document.querySelector('.bd-header__inner');
  
  if (headerInner) {
    const startItems = headerInner.querySelector('.navbar-header-items__start');
    const endItems = headerInner.querySelector('.navbar-header-items__end');
    
    if (startItems && endItems) {
      // Move search button container from end to start
      const searchContainer = endItems.querySelector('.navbar-persistent--container');
      if (searchContainer) {
        startItems.appendChild(searchContainer);
      }
      
      // Move repository icon links container from end to start
      const iconLinks = endItems.querySelector('.navbar-icon-links');
      if (iconLinks) {
        const iconLinksContainer = iconLinks.closest('.navbar-item');
        if (iconLinksContainer) {
          startItems.appendChild(iconLinksContainer);
        }
      }
    }
  }

  // Fetch GitHub API data
  fetchGitHubData();
});

async function fetchGitHubData() {
  try {
    // Fetch repository data
    const repoResponse = await fetch('https://api.github.com/repos/dell/omnia');
    const repoData = await repoResponse.json();
    
    // Fetch latest release data
    const releaseResponse = await fetch('https://api.github.com/repos/dell/omnia/releases/latest');
    const releaseData = await releaseResponse.json();
    
    // Update icon links with counts
    updateIconLinks(repoData, releaseData);
  } catch (error) {
    console.error('Error fetching GitHub data:', error);
  }
}

function updateIconLinks(repoData, releaseData) {
  const iconLinks = document.querySelectorAll('.navbar-icon-links .nav-link');
  
  iconLinks.forEach(link => {
    const title = link.getAttribute('title');
    const icon = link.querySelector('i');
    
    if (title === 'Stars' && repoData.stargazers_count !== undefined) {
      // Add star count
      const countSpan = document.createElement('span');
      countSpan.className = 'github-count';
      countSpan.textContent = formatNumber(repoData.stargazers_count);
      link.appendChild(countSpan);
    } else if (title === 'Forks' && repoData.forks_count !== undefined) {
      // Add fork count
      const countSpan = document.createElement('span');
      countSpan.className = 'github-count';
      countSpan.textContent = formatNumber(repoData.forks_count);
      link.appendChild(countSpan);
    } else if (title === 'Version' && releaseData.tag_name !== undefined) {
      // Add version number
      const versionSpan = document.createElement('span');
      versionSpan.className = 'github-count';
      versionSpan.textContent = releaseData.tag_name;
      link.appendChild(versionSpan);
    }
  });
}

function formatNumber(num) {
  if (num >= 1000) {
    return (num / 1000).toFixed(1) + 'k';
  }
  return num.toString();
}
