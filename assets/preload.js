(function () {
  const menuBarQuery        = '#pagelet_bluebar';
  const rightBarQuery       = '#rightCol';
  const dockQuery           = '#pagelet_dock';
  const loginBarQuery       = '.loggedout_menubar_container';
  const playButtonQuery     = '._bf8._1afk';
  const canvasQuery         = '._2v38';
  const replayButtonQuery   = '._5_5u';

  document.body.style.overflow = 'hidden';

  function init() {
    const loginBar = document.querySelector(loginBarQuery);

    if (!loginBar) {
      catchInterface();
      return;
    }

    const login_form = document.querySelector('#login_form');
    const email = document.querySelector('#email');
    const pass = document.querySelector('#pass');

    __endless_bot__getCredentials(function (credentials) {
      email.value = credentials[0];
      pass.value = credentials[1];

      console.log('submitted');
      login_form.submit();
    });
  }

  function catchInterface() {
    const menuBar = document.querySelector(menuBarQuery);
    const rightBar = document.querySelector(rightBarQuery);
    const dock = document.querySelector(dockQuery);

    if (!menuBar || !rightBar || !dock) {
      setTimeout(catchInterface, 100);
      return;
    }

    menuBar.remove();
    rightBar.remove();
    dock.remove();

    catchPlayButton();
  }

  function catchPlayButton() {
    if (window.location.href === 'https://www.facebook.com/') {
      window.location = 'https://apps.facebook.com/611307059053310';
      return;
    }

    const playButton = document.querySelector(playButtonQuery);
    const canvas = document.querySelector(canvasQuery);

    if (!playButton || !canvas) {
      setTimeout(catchPlayButton, 100);
      return;
    }

    canvas.style.left = '0';
    canvas.style.right = '360px';
    canvas.style.top = '50%';
    canvas.style.transform = 'translateY(-50%)';

    var rect = canvas.getBoundingClientRect();
    console.log(canvas);
    console.log(rect);

    playButton.click();
    __endless_bot__sendReady(function () {
      setTimeout(catchReplayButton, 250);
    });
  }

  function catchReplayButton() {
    const replayButton = document.querySelector(replayButtonQuery);

    if (!replayButton) {
      setTimeout(catchReplayButton, 250);
      return;
    }

    replayButton.click();
    setTimeout(catchReplayButton, 250);
  }

  init();
})();