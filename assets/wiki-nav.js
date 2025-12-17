(function() {
  'use strict';

  function initWikiNav() {
    const toggleButtons = document.querySelectorAll('.wiki-nav_toggle');
    const currentPath = window.location.pathname;

    toggleButtons.forEach(function(button) {
      button.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();

        const expanded = button.getAttribute('aria-expanded') === 'true';
        const targetId = button.getAttribute('aria-controls');
        const targetList = document.getElementById(targetId);
        const icon = button.querySelector('.wiki-nav_toggle-icon');

        if (targetList) {
          if (expanded) {
            button.setAttribute('aria-expanded', 'false');
            targetList.classList.add('wiki-nav_section--collapsed');
            if (icon) icon.textContent = '‹';
          } else {
            button.setAttribute('aria-expanded', 'true');
            targetList.classList.remove('wiki-nav_section--collapsed');
            if (icon) icon.textContent = '⌄';
          }
        }
      });
    });

    expandCurrentPath(currentPath);
  }

  function expandCurrentPath(currentPath) {
    const allLinks = document.querySelectorAll('.x-govuk-sub-navigation__link');
  
    allLinks.forEach(function(link) {
      if (link.getAttribute('href') === currentPath) {
        link.classList.add('wiki-nav_current-page');
        link.setAttribute('aria-current', 'page');
      
        const currentItem = link.closest('.wiki-nav_item');
      
        if (currentItem) {
          // Expand direct children of current page
          const directChildList = currentItem.querySelector(':scope > .wiki-nav_section');
          if (directChildList && directChildList.classList.contains('wiki-nav_section--collapsed')) {
            const listId = directChildList.getAttribute('id');
            const toggleButton = document.querySelector('[aria-controls="' + listId + '"]');
          
            if (toggleButton) {
              const icon = toggleButton.querySelector('.wiki-nav_toggle-icon');
              toggleButton.setAttribute('aria-expanded', 'true');
              directChildList.classList.remove('wiki-nav_section--collapsed');
              if (icon) icon.textContent = '⌄';
            }
          }
        }
      
        // Expand all parent/ancestor sections
        let parent = link.closest('.wiki-nav_item');
      
        while (parent) {
          const parentList = parent.closest('.wiki-nav_section');
          if (parentList && parentList.classList.contains('wiki-nav_section--collapsed')) {
            const listId = parentList.getAttribute('id');
            const toggleButton = document.querySelector('[aria-controls="' + listId + '"]');
          
            if (toggleButton) {
              const icon = toggleButton.querySelector('.wiki-nav_toggle-icon');
              toggleButton.setAttribute('aria-expanded', 'true');
              parentList.classList.remove('wiki-nav_section--collapsed');
              if (icon) icon.textContent = '⌄';
            }
          }
        
          parent = parentList ? parentList.closest('.wiki-nav_item') : null;
        }
      }
  });
}

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initWikiNav);
  } else {
    initWikiNav();
  }
})();
