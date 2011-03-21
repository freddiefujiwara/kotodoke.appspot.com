/**
 * The markers array.
 * @type {Object}
 */
var markers = {
  'shelters': [
   {% for shelter in shelters %}
    {
      'name': '{{ shelter.name }}',
      'prefecture': '{{ shelter.prefecture }}',
      'city': '{{ shelter.city }}',
      'id': '{{ shelter.shelter_id }}',
      'location': [{{ shelter.lat }}, {{ shelter.lng }}]
    },
   {% endfor %}
  ]
};
