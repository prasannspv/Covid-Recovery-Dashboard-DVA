var observer = new MutationObserver(function (mutations, me) {
  var new_cases = document.getElementById('new_cases');
  if (new_cases) {
    handleLoadOfChoropleth(new_cases);
    me.disconnect();
    return;
  }
});

function handleLoadOfChoropleth(new_cases) {
    new_cases.on('plotly_click', function (point) {
        document.getElementById("kpi-country").value = point.points[0].location;
        console.log(point.points[0].location);
        document.getElementById('kpi-country').dispatchEvent(new Event('click'));
    });
}

observer.observe(document, {
  childList: true,
  subtree: true
});
