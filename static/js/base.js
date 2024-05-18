document.addEventListener('DOMContentLoaded', function() {
  var body = document.body;
  var footer = document.querySelector('.footer');
  var toggleButton = document.querySelector('#dark-mode-toggle');

  // Check local storage for dark mode setting, default to dark mode if not set
  if (localStorage.getItem('darkMode') === null) {
      localStorage.setItem('darkMode', 'true');
  }

  // Apply dark mode based on local storage setting
  if (localStorage.getItem('darkMode') === 'true') {
      body.classList.add('dark-mode');
      footer.classList.add('dark-mode');
  }

  // Handle button click
  toggleButton.addEventListener('click', function() {
      body.classList.toggle('dark-mode');
      footer.classList.toggle('dark-mode');

      // Save dark mode setting in local storage
      if (body.classList.contains('dark-mode')) {
          localStorage.setItem('darkMode', 'true');
      } else {
          localStorage.setItem('darkMode', 'false');
      }
  });
});
