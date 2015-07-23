(function($) {
  $(document).ready(function() {
    // var funding_inline = ;
    $('.new_initiative_party_text').after($('#projectfunding_set-group').detach());
    $('.phd_research').after($('#phdstudent_set-group').detach());
    $('#phdstudent_set-group').after($('#projectoutput_set-group').detach());
    $('.new_courses').after($('#newcoursedetail_set-group').detach());
    $('.course_requirement').after($('#coursereqdetail_set-group').detach());
    $('.external_collaboration').after($('#collaborators_set-group').detach());
  });
})(django.jQuery);



