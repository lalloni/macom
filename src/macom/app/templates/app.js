isc.DataSource.create({
	ID : "ds_model",
	dataURL : "{% url api_model %}",
	dataFormat : "json",
	fields : [
        { name : "name" },
        { name : "name" }
    ]
});

isc.VLayout.create({
	width : "100%",
	height : "100%",
	members : [ isc.HStack.create({
		ID : "HeaderBar",
		height : "30px",
		members : [ isc.Label.create({
			contents : "macom"
		}) ]
	}), isc.HLayout.create({
		height : "*",
		members : [ isc.TreeGrid.create({
            dataSource : "ds_model",
			autoFetchData : true,
            loadDataOnDemand: false,
            defaultIsFolder:false,
			showResizeBar : true,
            generateClickOnEnter: true,
            fields: [
                { name: 'name' ,
                    recordDoubleClick: openTab }
            ],
		}), isc.TabSet.create({
			ID: 'contentTabs'
		}) ]
	}), isc.HStack.create({
		ID : "BottomToolBar",
		height : "1",
		members : [ isc.IButton.create({
			title : "Console",
			click : "isc.showConsole()"
		}) ]
	}) ]
});

function openTab (viewer, record, recordNum, field, fieldNum, value, rawValue) {
    // buscar tab q tenga el mismo record
    var tab;
    for ( i=0; i < contentTabs.tabs.length; i++ ) {
        var t = contentTabs.getTab(i);
        if ( t.record == record ) {
            tab = t;
            break;
        }
    }
    
    // si no se encuentra generar uno nuevo con titulo = record.name
    if ( !tab ){
        contentTabs.addTab( {
            title: record.name,
            record : record
        } );
        tab = contentTabs.getTab(contentTabs.tabs.length-1);
    }

    contentTabs.selectTab( tab );
}
