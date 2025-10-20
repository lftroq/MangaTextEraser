jQuery(document).ready(function () {
  ImgUpload();
});

function ImgUpload() {
  var imgWrap = "";
  var imgArray = []; // Main storage for all files

  function init() {
    bindEvents();
    updateProcessButton();
  }

  function bindEvents() {
    // File input change handler
    $('.upload__inputfile').on('change', function (e) {
      handleFiles(e);
    });

    // Form submit handler
    $('form').on('submit', function(e) {
      updateFileInput(); // Final sync before submission
    });

    // Image removal
    $('body').on('click', ".upload__img-close", function (e) {
      var fileName = $(this).data("file");
      removeFile(fileName);
    });
  }

  function handleFiles(e) {
    imgWrap = $('.upload__img-wrap');
    var maxLength = parseInt($('.upload__inputfile').attr('data-max_length'));
    var files = e.target.files;
    var filesArr = Array.prototype.slice.call(files);

    filesArr.forEach(function (f) {
      if (!f.type.match('image.*')) return;

      if (imgArray.length >= maxLength) {
        alert(`Maximum ${maxLength} images allowed`);
        return false;
      }

      if (!fileExists(f)) {
        imgArray.push(f);
        renderPreview(f);
      }
    });

    updateProcessButton();
  }

  function fileExists(newFile) {
    return imgArray.some(
      existing => 
        existing.name === newFile.name && 
        existing.size === newFile.size &&
        existing.lastModified === newFile.lastModified
    );
  }

  function renderPreview(file) {
    var reader = new FileReader();
    reader.onload = function (e) {
      var html = `
        <div class='upload__img-box'>
          <div style='background-image: url(${e.target.result})' 
               data-file='${file.name}' 
               class='img-bg'>
            <div class='upload__img-close' data-file='${file.name}'></div>
          </div>
        </div>
      `;
      $('.upload__img-wrap').append(html);
    };
    reader.readAsDataURL(file);
  }

  function removeFile(fileName) {
    imgArray = imgArray.filter(f => f.name !== fileName);
    $(`[data-file="${fileName}"]`).closest('.upload__img-box').remove();
    updateProcessButton();
  }

  function updateProcessButton() {
    $('#processWrapper').toggle(imgArray.length > 0);
    updateFileInput();
  }

  function updateFileInput() {
    var fileInput = $('.upload__inputfile')[0];
    var dataTransfer = new DataTransfer();
    imgArray.forEach(file => dataTransfer.items.add(file));
    fileInput.files = dataTransfer.files;
  }

  // ===== DRAG AND DROP =====
  const dropZone = document.getElementById('dropZone');
  const fileInput = document.getElementById('fileInput');

  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, preventDefaults, false);
  });

  ['dragenter', 'dragover'].forEach(eventName => {
    dropZone.addEventListener(eventName, highlight, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    dropZone.addEventListener(eventName, unhighlight, false);
  });

  dropZone.addEventListener('drop', function(e) {
    var dt = e.dataTransfer;
    fileInput.files = dt.files;
    var event = new Event('change');
    fileInput.dispatchEvent(event);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  function highlight() {
    dropZone.classList.add('dragover');
  }

  function unhighlight() {
    dropZone.classList.remove('dragover');
  }

  dropZone.addEventListener('click', () => fileInput.click());

  init();
}