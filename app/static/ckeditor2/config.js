// /**
//  * @license Copyright (c) 2003-2017, CKSource - Frederico Knabben. All rights reserved.
//  * For licensing, see LICENSE.md or http://ckeditor.com/license
//  */
//
// CKEDITOR.editorConfig = function( config ) {
// 	// Define changes to default configuration here.
// 	// For complete reference see:
// 	// http://docs.ckeditor.com/#!/api/CKEDITOR.config
//
// 	// The toolbar groups arrangement, optimized for two toolbar rows.
// 	config.toolbarGroups = [
// 		//{ name: 'clipboard',   groups: [ 'clipboard', 'undo' ] },
// 		//{ name: 'editing',     groups: [ 'find', 'selection', 'spellchecker' ] },
// 		//{ name: 'links' },
// 		{ name: 'insert' },
// 		{ name: 'forms' },
// 		//{ name: 'tools' },
// 		{ name: 'document',	   groups: [ 'mode', 'document', 'doctools' ] },
// 		//{ name: 'others' },
// 		//'/',
// 		{ name: 'basicstyles', groups: [ 'basicstyles', 'cleanup' ] },
// 		{ name: 'paragraph',   groups: [ 'list', 'indent', 'blocks', 'align', 'bidi' ] },
// 		{ name: 'styles' },
// 		//{ name: 'colors' }
// 	];
//
// 	// Remove some buttons provided by the standard plugins, which are
// 	// not needed in the Standard(s) toolbar.
// 	config.removeButtons = 'Underline,Subscript,Superscript';
//
// 	// Set the most common block elements.
// 	config.format_tags = 'p;h1;h2;h3;pre';
//
// 	config.language = 'en';
// 	// Simplify the dialog windows.
// 	config.removeDialogTabs = 'image:advanced;link:advanced';
// 	config.extraPlugins = 'imagepaste,uploadimage,image2';
// 	config.filebrowserImageUploadUrl = '/Home/UploadRichEditorFile';
//
// 	config.uploadUrl = '/Home/UploadRichEditorPasteImg';
// };


/**
 * @license Copyright (c) 2003-2017, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function (config) {
    // Define changes to default configuration here. For example:
    // config.language = 'fr';
    // config.uiColor = '#AADC6E';

    config.extraPlugins = "CodePlugin,imagepaste,uploadimage,image2";
	//    "imagepaste, uploadimage,image2";
    // config.filebrowserImageUploadUrl = '/ckupload/';
    config.filebrowserUploadUrl = '/ckupload/';
    config.uploadUrl = "/ckupload_pasteimg/";
    config.toolbarCanCollapse = true;   // 工具栏是否可被收缩
    config.image_previewText = ''; //清空预览区域显示内容
    config.font_names = '宋体/SimSun;新宋体/NSimSun;仿宋/FangSong;楷体/KaiTi;仿宋_GB2312/FangSong_GB2312;' +
        '楷体_GB2312/KaiTi_GB2312;黑体/SimHei;华文细黑/STXihei;华文楷体/STKaiti;华文宋体/STSong;华文中宋/STZhongsong;' +
        '华文仿宋/STFangsong;华文彩云/STCaiyun;华文琥珀/STHupo;华文隶书/STLiti;华文行楷/STXingkai;华文新魏/STXinwei;' +
        '方正舒体/FZShuTi;方正姚体/FZYaoti;细明体/MingLiU;新细明体/PMingLiU;微软雅黑/Microsoft YaHei;微软正黑/Microsoft JhengHei;' +
        'Arial Black/Arial Black;' + config.font_names;
    // config.toolbarStartupExpanded = false;

    config.toolbar = [
        {name: 'document', items: ['Source', '-', 'Code', 'Preview', '-', 'Maximize']},
        { name: 'editing', items : [ 'Find','Replace','-','SelectAll','-','SpellChecker', 'Scayt' ] },
        {name: 'clipboard', items: ['Undo', 'Redo', '-', 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord']},
        {name: 'basicstyles', items: ['Bold', 'Italic', 'Underline', 'Strike', '-', 'RemoveFormat']},
        {name: 'paragraph', items: ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']},
        {name: 'links', items: ['Link', 'Unlink', 'Anchor']},
        {name: 'insert', items: ['Image', 'Table', 'HorizontalRule', 'Smiley']},
        {name: 'styles', items: ['Styles', 'Format', 'Font', 'FontSize']},
        {name: 'colors', items: ['TextColor', 'BGColor']}
    ];
    config.height = 600;

};
