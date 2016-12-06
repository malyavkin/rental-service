let monthsFull= ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
                 'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'];
monthsShort= ['янв', 'фев', 'мар', 'апр', 'мая', 'июня',
              'июля', 'авг', 'сен', 'окт', 'ноя', 'дек'];
weekdaysFull= [ 'воскресенье', 'понедельник', 'вторник',
                'среда', 'четверг', 'пятница', 'суббота'];
weekdaysShort= ['вс', 'пн', 'вт', 'ср', 'чт', 'пт', 'сб'];
format= 'dd mmm yyyy';
formatSubmit= 'yyyy-mm-dd';
$(document).ready(function() {
    $('select').material_select();
    $('.scrollspy').scrollSpy();
    $('.datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 15, // Creates a dropdown of 15 years to control year
        format: formatSubmit,
        formatSubmit: formatSubmit,
        monthsFull: monthsFull,
        monthsShort: monthsShort,
        weekdaysFull: weekdaysFull,
        weekdaysShort: weekdaysShort
    });
    $('.aged_datepicker').pickadate({
        selectMonths: true, // Creates a dropdown to control month
        selectYears: 140, // Creates a dropdown of 15 years to control year
        format: formatSubmit,
        formatSubmit: formatSubmit,
        monthsFull: monthsFull,
        monthsShort: monthsShort,
        weekdaysFull: weekdaysFull,
        weekdaysShort: weekdaysShort
    });
    $("#select_booked_class").change(function(){
        console.log($(this).val())
    })

    // table of contents
    setTimeout(function() {
      var tocWrapperHeight = 260; // Max height of ads.
      var tocHeight = $('.toc-wrapper .table-of-contents').length ? $('.toc-wrapper .table-of-contents').height() : 0;
      var socialHeight = 95; // Height of unloaded social media in footer.
      var footerOffset = $('body > footer').first().length ? $('body > footer').first().offset().top : 0;
      var bottomOffset = footerOffset - socialHeight - tocHeight - tocWrapperHeight;

      if ($('nav').length) {
        $('.toc-wrapper').pushpin({
          top: $('nav').height(),
          bottom: bottomOffset
        });
      }
      else if ($('#index-banner').length) {
        $('.toc-wrapper').pushpin({
          top: $('#index-banner').height(),
          bottom: bottomOffset
        });
      }
      else {
        $('.toc-wrapper').pushpin({
          top: 0,
          bottom: bottomOffset
        });
      }
    }, 100);
    $("ul.dropdown-content[data-copy-selected]").each(function(i, v){
        let inputname = $(v).data("copy-selected")
        $(">li", v).click(function(){
            let value = $(this).data("value")
            $("input[name="+inputname+"]").val(value)
            Materialize.updateTextFields();
        })
    })


});