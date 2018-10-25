(function () {

 b = 'CodePlugin';

 CKEDITOR.plugins.add(b, {

       // requires: ['styles', 'button'],

       init: function (a) {

               a.addCommand(b, CKEDITOR.plugins.autoformat.commands.autoformat);

               a.ui.addButton('Code', {

                      label: "一键排版",

                      command: 'CodePlugin',

                      icon: this.path + "toys.png"

          });

       }

 });

 CKEDITOR.plugins.autoformat = {

     commands: {

          autoformat: {

                exec: function (editor) {

                     formatText(editor);

               }

         }

    }

};

  //执行的方法
    function formatText() {
        var content = editor1.getData();
        //clearScript
        content = content.replace(/\<\!\-\-(.*?)\-\-\>/gi, '');
        content = content.replace(/<[\s]*(script)[^>]*>.*?<[\s]*\/[\s]*(script)[\s]*>/gi, '');
        content = content.replace(/<[\s]*(style|title)[^>]*>.*?<[\s]*\/[\s]*(style|title)[\s]*>/gi, '');
        content = content.replace(/<[\s]*(meta|link|base)[^>]*>/gi, '');
        //clearAttr
        content = content.replace(/(id|class|style|onclick|alt|title|width|height|_href|_src)\s*\=\'[^\>\']*?\'/gi, '');
        content = content.replace(/(id|class|style|onclick|alt|title|width|height|_href|_src)\s*\=\"[^\>\"]*?\"/gi, '');
        //content = content.replace(/(id|class|style|onclick|alt|title|width|height|_href|_src)\s*\=[^\>\s]+?/gi,'');

        //clearLine
        content = content.replace(/[\s]+/gi, ' ');
        content = content.replace(/[\s]+>/gi, '>');
        content = content.replace(/<([\/\s]*)(div)([^>]*)>/gi, '<$1p$3>');
        content = content.replace(/(<([\/\s]*)([^>]*)>)(\s|&nbsp;|\　|\ )+/gi, '$1');
        content = content.replace(/(\s*<[\s]*br[^>]*>\s*)+/gi, '<br/>');
        content = content.replace(/(^\s*<[\s]*br[^>]*>|<[\s]*br[^>]*>\s*$)/gi, '');
        content = content.replace(/(<[\/\s]*(p|hr|h1|h2|h3|h4|h5|h6)[^>]*>)\s*(<[\s]*br[^>]*>)/gi, '$1');
        content = content.replace(/(<[\s]*br[^>]*>)\s*(<[\/\s]*(p|hr|h1|h2|h3|h4|h5|h6)[^>]*>)/gi, '$2');
        contentre = content.replace(/<(!=iframe|embed|br|hr|tr|td)[^>]+>\s*<[\s]*\/[\s]*(!=iframe|embed|br|hr|tr|td)[^>]+>/gi, '');
        while(contentre != content) {
            content = contentre;
            contentre = content.replace(/<(!=iframe|embed|br|hr|tr|td)[^>]+>\s*<[\s]*\/[\s]*(!=iframe|embed|br|hr|tr|td)[^>]+>/gi, '');
        }
        content = content.replace(/<([\/\s]*)(p)([^>]*)>(\s*<[^>]*(br)[^>]+>\s*)*<([\/\s]*)\/([\/\s]*)(p)([^>]*)>/gi, '');
        content = content.replace(/(<[\s]*p[^>]*>[\s]*)*(<[\s]*(embed|img|iframe)[^>]*>)([\s]*<[\s]*\/[\s]*p[^>]*>)*/gi, '<div style="text-align: center;">$2</div>');
        //clearA
        content = content.replace(/<([\/\s]*)(a)([^>]*)>/gi, '');
        //content = content.replace(/<([\/\s]*)(a)([^>]*)(!=href\=\"\/|href\=\'\/|href\=\/)([^>]*)>/gi,'');
        editor1.setData(content);
    }
 })();