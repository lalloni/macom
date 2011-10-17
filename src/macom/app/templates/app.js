isc.DataSource.create({
	ID : "ds_model",
	dataURL : "{% url api_model %}",
	dataFormat : "json",
	fields : [
        { name : "name" },
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
            width: '300px',
            dataSource : "ds_model",
			autoFetchData : true,
            loadDataOnDemand: false,
            defaultIsFolder: false,
			showResizeBar : true,
            generateClickOnEnter: true,
            fields: [
                { name: 'name' ,
                    recordDoubleClick: openTab }
            ],
            }), isc.TabSet.create({
                ID: 'contentTabs'
            }) 
        ]
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
            title: getTitle(record) + rawValue,
            record : record,
            canClose: true,
            pane: nodeContent(record)
        } );
        tab = contentTabs.getTab(contentTabs.tabs.length-1);
    }

    contentTabs.selectTab( tab );
}

function getTitle( record ){
    if ( record._parent_isc_ResultTree_0.name ) return getTitle( record._parent_isc_ResultTree_0 ) + record._parent_isc_ResultTree_0.name + ":";
    return "";
}

function nodeContent( record ) {
    switch ( record.type ) {
        case 'system':
            return isc.DynamicForm.create({
                    autoFetchData: true,
                    canEdit: false,
                    dataSource: isc.DataSource.create({
                        dataURL: record.readurl,
                        dataFormat : "json",
                        dataProtocol: "getParams"
                    }),
                    fields: [
                        { name:"name", type:"text", title:"Nombre", width: "*"},
                        { name:"description", type:"textArea", title:"Descripción", width: "*"},
                        { name:"referents", type:"textArea", title:"Referentes", width: "*"},
                        { name:"documentation", type:"textArea", title:"Documentación", width: "*"},
                        { name:"external", type:"checkbox", title:"Externo", width: "*"}
                    ]
            });

            break;
        case 'module':
            return isc.DynamicForm.create({
                    autoFetchData: true,
                    canEdit: false,
                    dataSource: isc.DataSource.create({
                        dataURL: record.readurl,
                        dataFormat : "json",
                        dataProtocol: "getParams",
                        fields: [
                            { name: "system", valueXPath: "system/name" }
                        ]
                    }),
                    fields: [
                        { name:"system", type:"textArea", title:"Sistema", width: "*"},    
                        { name:"name", type:"text", title:"Nombre", width: "*"},
                        { name:"goal", type:"textArea", title:"Objetivo", width: "*"},
                        { name:"referents", type:"textArea", title:"Referentes", width: "*"},
                        { name:"documentation", type:"textArea", title:"Documentación", width: "*"},
                        { name:"external", type:"checkbox", title:"Externo", width: "*"},
                        { name:"criticity", type:"text",title:"Criticidad"}
                    ]
            });
            break;
        case 'interface':
            return isc.DynamicForm.create({
                    autoFetchData: true,
                    canEdit: false,
                    dataSource: isc.DataSource.create({
                        dataURL: record.readurl,
                        dataFormat : "json",
                        dataProtocol: "getParams",
                        fields: [
                            { name: "module", valueXPath: "module/name" }
                        ]
                    }),
                    fields: [
                        { name:"module", type:"text", title:"Módulo", width: "*"},    
                        { name:"name", type:"text", title:"Nombre", width: "*"},
                        { name:"goal", type:"textArea", title:"Objetivo", width: "*"},
                        { name:"referents", type:"textArea", title:"Referentes", width: "*"},
                        { name:"documentation", type:"textArea", title:"Documentación", width: "*"},
                        { name:"technology", type:"textArea", title:"Tecnología", width: "*"},
                        { name:"direction_inbound", type:"checkbox", title:"Entrada", width: "*"},
                        { name:"direction_outbound", type:"checkbox", title:"Salida", width: "*"},
                    ]
            });
            break;
    }
}
