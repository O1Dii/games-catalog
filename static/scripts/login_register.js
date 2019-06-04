$(function() {
  $("#birthday").datepicker({
    orientation: "top auto",
    maxDate: "0",
    changeMonth: true,
    changeYear: true,
    dateFormat: 'dd.mm.yy',
    closeText: 'Закрыть',
    currentText: 'Сегодня',
    monthNamesShort: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
    dayNamesShort: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
    dayNamesMin: ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'],
    autoclose: true,
  });
});