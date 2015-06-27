var myCodeMirror = CodeMirror.fromTextArea(document.getElementById("id_source"), {
    lineNumbers: true,
    mode: 'python',
    indentWithTabs: false,
    indentUnit: 4
});

$(function() {
    var assignmentsModal = $('.js-assignment-modal').modal({
        show: false
    });
    var originalSourceCoudeButton = $('.js-use-original-source-code-button');
    originalSourceCoudeButton.on('click', function(evt){
        evt.preventDefault();
        var originalSourceCode = $('.js-original-source-code').html();
        myCodeMirror.setValue(originalSourceCode);
        originalSourceCoudeButton.hide();
    });
    $('.js-prompt-previously-solved-assignment').on('click', function(evt){
        evt.preventDefault();
        var self = $(this);
        var attemptId = self.data('attempt-id');
        var attemptSource = $('#assignment-source-' + attemptId).html();
        var attemptSourceVerbatim = $('#assignment-source-' + attemptId + '-verbatim').html();
        var attemptTitle = self.html();
        assignmentsModal.find('.js-assignment-modal-title').html(attemptTitle);
        assignmentsModal.find('.modal-body').html(attemptSource);
        assignmentsModal.modal('show');

        $('.js-use-source-code').on('click', function(evt){
            evt.preventDefault();
            myCodeMirror.setValue(attemptSourceVerbatim);
            assignmentsModal.modal('hide');
            originalSourceCoudeButton.show();
        });
    });

    $('.js-show-execution-errors').on('click', function(evt){
        $('pre.execution-traceback').toggle();
    });
});
