$(document).on("click", ".alert", function(e) {
    bootbox.dialog({
        title: "コミュニティの作成",
        message: '<div class="row">  ' +
            '<div class="col-md-12"> ' +
            '<form class="form-horizontal" name="form1" id="form1" method="post" action="{{ reverse_url('groups') }}"> ' +
            '{% module xsrf_form_html() %} ' +
            '<div class="form-group"> ' +
            '<label class="col-md-4 control-label" for="name">グループ名</label> ' +
            '<div class="col-md-4"> ' +
            '<input id="name" name="name" type="text" placeholder="Group name" class="form-control input-md"> ' +
            '<!--<span class="help-block">Here goes your name</span>--> </div> ' +
            '</div> ' +
            '<div class="form-group"> ' +
            '<label class="col-md-4 control-label" for="awesomeness">公開条件</label> ' +
            '<div class="col-md-4"> <div class="radio"> <label for="awesomeness-0"> ' +
            '<input type="radio" name="awesomeness" id="awesomeness-0" value="Really awesome" checked="checked"> ' +
            '公開 </label> ' +
            '</div><div class="radio"> <label for="awesomeness-1"> ' +
            '<input type="radio" name="awesomeness" id="awesomeness-1" value="Super awesome"> 非公開 </label> ' +
            '</div> ' +
            '</div> </div>' +
            '</form> </div>  </div>',
        buttons: {
            success: {
                label: "Save",
                className: "btn-success",
                callback: function () {
                $('#form1').submit();
                    var name = $('#name').val();
                    var answer = $("input[name='awesomeness']:checked").val()
                    Example.show("Hello " + name + ". You've chosen <b>" + answer + "</b>");
                }
            }
        }
    }
);
});