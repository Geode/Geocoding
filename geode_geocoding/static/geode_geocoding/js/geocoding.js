function showadresse(url, html_elem_id){
    var input = $("#" + html_elem_id);

    var bestAdresses = new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
            url: url+"?adr=%QUERY",
            wildcard: '%QUERY',
            transform : function(response) {
                return $.map(response.result, function(item) {
                    return item;
                })
            }
        }
    });

    input.typeahead({
        minLength: 3,
        highlight: true,
        items: 5
    },{
        name: 'address',
        display: function(data) {
            return "(" + data.address.street.municipality + ") " + data.address.street.name + " " + data.address.number;
        },
        source: bestAdresses
    });
};
