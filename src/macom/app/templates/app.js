isc.DataSource.create({
	ID : "ds_model",
	dataURL : "{% url api_model %}",
	dataFormat : "json",
	fields : [ {
		name : "name"
	}, ]
});

isc.VLayout.create({
	width : "100%",
	height : "100%",
	members : [ isc.HStack.create({
		ID : "HeaderSection",
		height : 48,
		hPolicy : "fill",
		members : [ isc.Label.create({
			contents : "macom",
			baseStyle : "header"
		}), isc.LayoutSpacer.create({
			width : "*"
		}), isc.Img.create({
			src : "grass.png",
			imageType : "normal"
		}) ]
	}), isc.HLayout.create({
		ID : "ContentSection",
		height : "*",
		showEdges : "true",
		members : [ isc.TreeGrid.create({
			ID : "NavigationTree",
			width : 300,
			dataSource : "ds_model",
			autoFetchData : true,
			loadDataOnDemand : false,
			defaultIsFolder : false,
			showResizeBar : true,
			generateClickOnEnter : true,
			fields : [ {
				name : 'name',
				recordDoubleClick : openTab
			} ],
		}), isc.TabSet.create({
			ID : 'ContentTabSet'
		}) ]
	}), isc.HStack.create({
		ID : "FooterSection",
		height : "1",
		members : [ isc.IButton.create({
			title : "Console",
			click : "isc.showConsole()"
		}) ]
	}) ]
});

function openTab(viewer, record, recordNum, field, fieldNum, value, rawValue) {
	// buscar tab q tenga el mismo record
	var tab = ContentTabSet.tabs.filter(function(e) {
		e.record == record
	})[0];
	// si no se encuentra generar uno nuevo con titulo = record.name
	if (typeof (tab) == 'undefined') {
		ContentTabSet.addTab({
			title : rawValue,
			record : record,
			canClose : true,
			pane : nodeContent(record)
		});
		tab = ContentTabSet.getTab(ContentTabSet.tabs.length - 1);
	}
	ContentTabSet.selectTab(tab);
}

function nodeContent(record) {
	switch (record.type) {
	case 'system':
		return isc.DynamicForm.create({
			autoFetchData : true,
			canEdit : false,
			dataSource : isc.DataSource.create({
				dataURL : record.readurl,
				dataFormat : "json",
				dataProtocol : "getParams"
			}),
			fields : [ {
				name : "name",
				type : "text",
				title : "Nombre",
				width : "*"
			}, {
				name : "description",
				type : "textArea",
				title : "Descripción",
				width : "*"
			}, {
				name : "referents",
				type : "textArea",
				title : "Referentes",
				width : "*"
			}, {
				name : "documentation",
				type : "textArea",
				title : "Documentación",
				width : "*"
			}, {
				name : "external",
				type : "checkbox",
				title : "Externo",
				width : "*"
			} ]
		});

		break;
	case 'module':
		return isc.DynamicForm.create({
			autoFetchData : true,
			canEdit : false,
			dataSource : isc.DataSource.create({
				dataURL : record.readurl,
				dataFormat : "json",
				dataProtocol : "getParams",
				fields : [ {
					name : "system",
					valueXPath : "system/name"
				} ]
			}),
			fields : [ {
				name : "system",
				type : "textArea",
				title : "Sistema",
				width : "*"
			}, {
				name : "name",
				type : "text",
				title : "Nombre",
				width : "*"
			}, {
				name : "goal",
				type : "textArea",
				title : "Objetivo",
				width : "*"
			}, {
				name : "referents",
				type : "textArea",
				title : "Referentes",
				width : "*"
			}, {
				name : "documentation",
				type : "textArea",
				title : "Documentación",
				width : "*"
			}, {
				name : "external",
				type : "checkbox",
				title : "Externo",
				width : "*"
			}, {
				name : "criticity",
				type : "text",
				title : "Criticidad"
			} ]
		});
		break;
	case 'interface':
		return isc.DynamicForm.create({
			autoFetchData : true,
			canEdit : false,
			dataSource : isc.DataSource.create({
				dataURL : record.readurl,
				dataFormat : "json",
				dataProtocol : "getParams",
				fields : [ {
					name : "module",
					valueXPath : "module/name"
				} ]
			}),
			fields : [ {
				name : "module",
				type : "text",
				title : "Módulo",
				width : "*"
			}, {
				name : "name",
				type : "text",
				title : "Nombre",
				width : "*"
			}, {
				name : "goal",
				type : "textArea",
				title : "Objetivo",
				width : "*"
			}, {
				name : "referents",
				type : "textArea",
				title : "Referentes",
				width : "*"
			}, {
				name : "documentation",
				type : "textArea",
				title : "Documentación",
				width : "*"
			}, {
				name : "technology",
				type : "textArea",
				title : "Tecnología",
				width : "*"
			}, {
				name : "direction_inbound",
				type : "checkbox",
				title : "Entrada",
				width : "*"
			}, {
				name : "direction_outbound",
				type : "checkbox",
				title : "Salida",
				width : "*"
			}, ]
		});
		break;
	}
}
