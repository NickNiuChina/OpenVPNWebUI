$(document).ready(function() {
    function createEditor(name, size, theme, mode, readonly) {
      // find the textarea
      var textarea = document.querySelector("form textarea[name=" + name + "]");

      // create ace editor
      var editor = ace.edit()
      editor.container.style.height = size

      editor.setTheme("ace/theme/" + theme); //"clouds_midnight"
      //editor.setTheme("ace/theme/twilight");
      //editor.setTheme("ace/theme/iplastic");

      editor.session.setMode("ace/mode/" + mode);

      editor.setReadOnly(readonly);
      editor.setShowPrintMargin(false);
      editor.session.setUseWrapMode(true);
      editor.session.setValue(textarea.value)
      // replace textarea with ace
      textarea.parentNode.insertBefore(editor.container, textarea)
      textarea.style.display = "none"
      // find the parent form and add submit event listener
      var form = textarea
      while (form && form.localName != "form") form = form.parentNode
      form.addEventListener("submit", function() {
          // update value of textarea to match value in ace
          textarea.value = editor.getValue()
      }, true)
    };

	  // Check if "themeEditor" is set in localStorage
	  if (localStorage.getItem("theme") === "dark") {
		createEditor("Logs", "700px", "clouds_midnight", "ovpn", true);
	  } else {
		createEditor("Logs", "700px", "clouds", "ovpn", true);
	  }

});