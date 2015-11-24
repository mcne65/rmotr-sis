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
    var originalSourceCodeButton = $('.js-use-original-source-code-button');
    originalSourceCodeButton.on('click', function(evt){
        evt.preventDefault();
        var originalSourceCode = $('.js-original-source-code').html();
        myCodeMirror.setValue(originalSourceCode);
        originalSourceCodeButton.hide();
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
            originalSourceCodeButton.show();
        });
    });

    // toggle row with execution errors
    $('.js-show-execution-errors').on('click', function(evt){
        $('pre.execution-traceback').toggle();
    });

    // show modal with test cases
    var testCasesModal = $('.js-test-cases-modal').modal({
        show: false
    });
    $('.js-show-test-cases-modal').on('click', function(evt){
        testCasesModal.modal('show');
    });

    // show modal with solution
    var solutionModal = $('.js-solution-modal').modal({
        show: false
    });
    $('.js-show-solution-modal').on('click', function(evt){
        solutionModal.modal('show');
    });
});
