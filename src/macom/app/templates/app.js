isc.DataSource.create({
	ID : "ds_model",
	dataURL : "{% url api_model %}",
	dataFormat : "json",
	fields : [ {
		"name" : "name"
	} ]
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
			showResizeBar : true,
		}), isc.TabSet.create({
			tabs : [ {
				title : "Prueba 1",
				pane : isc.Label.create({
					contents : "Contenido 1"
				})
			}, {
				title : "Prueba 2",
				pane : isc.Label.create({
					contents : "Contenido 2"
				})
			}, {
				title : "Prueba 3",
				pane : isc.HTMLFlow.create({
					contentsURL : "{% url system_detail '1' %}"
				})
			}, {
				title : "Prueba 4",
				pane : isc.Label.create({
					contents : "Contenido 4"
				})
			} ]
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
