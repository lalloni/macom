//Settings
var diagramServiceUrl = "{{diagram_service_url}}/"+window.location.protocol+"//"+window.location.host;

// Fields Predefinidos
var fieldFullName = { name : "full_name", title : "Nombre" };
var fieldDescription = { name : "description", title : "Descripci&oacute;n" };
var fieldGoal = { name : "goal", title : "Objetivo" };
var fieldReferents = { name : "referents", title : "Referentes" };
var fieldDocumentation = { name : "documentation", title : "Documentaci&oacute;n" };
var fieldTechnology = { name : "technology", title : "Tecnolog&iacute;a", width: "100" };
var fieldDirection = { name : "direction", title : " ", width: "20", type:"image", imageURLPrefix:"/media/img/morocho/icon", imageURLSuffix:".png" };
var fieldExternal = { name : "external", title : " ", width: "20", type:"image", imageURLPrefix:"/media/img/external", imageURLSuffix:"-icon.gif" };

// Propiedades default en objetos de SmartClient
isc.defineClass("Diagram", "Img").addProperties({
    imageType : "natural",
    height: "*"
});

isc.DetailViewer.addProperties({
    autoFetchData : true
})

// Objetos predefinidos
isc.defineClass("DetailGrid", "ListGrid").addProperties({
    recordDoubleClick: openTab,
    alternateRecordStyles:true,
    autoFetchData : true,
    showFilterEditor: true,
    filterOnKeypress: true
});

isc.defineClass("DetailGridInterface", "DetailGrid").addProperties({
    fields : [ fieldDirection, fieldFullName, fieldTechnology, fieldGoal ]
});

isc.defineClass("JsonDataSource", "DataSource").addProperties({
    dataFormat : "json",
    dataProtocol : "getParams"
});

// APPLICATION

function openTab(viewer, record, recordNum, field, fieldNum, value, rawValue) {	// buscar tab q tenga el mismo record
    var tab = ContentTabSet.getTab(record.resource_uri);

	// si no se encuentra generar uno nuevo con titulo = record.name
	if ( tab == null || typeof (tab) == 'undefined') {
        ContentTabSet.addTab({
			ID: record.resource_uri,
            title : ( record.full_name.length > 40 ? "... " + record.full_name.substring(record.full_name.length - 40) : record.full_name ),
			record : record,
			canClose : true
		});
        // Busca el tab recien creado
		tab = ContentTabSet.getTab(record.resource_uri);

        // Se fija el record.kind
        switch (record.kind){
            case 'root': // Si es root:
                // muetra items del root
                showViewRoot(tab, record);
                break;
            
            default: // Si es system, module, dependency o interface
                // DATASOURCE
                isc.JsonDataSource.create({
                    ID : record.resource_uri,
                    dataURL : record.resource_uri
                });
                
                // VIEW
                isc.DataSource.get(record.resource_uri)
                    .fetchData(null,
                                    "showView"+record.kind.charAt(0).toUpperCase() + record.kind.slice(1).toLowerCase()+"(data, \""+ record.resource_uri +"\")" // Callback
                );
        }
	 }
	ContentTabSet.selectTab(tab);
 }


function showViewRoot ( tab, record ){
    var tabset = new Array();

    for  ( var i = 0; i < record.diagrams.length; i++ ){
        tabset.push ({
            title: record.diagrams[i].name,
            pane:  isc.Diagram.create({
                src: diagramServiceUrl+record.diagrams[i].diagram_uri
            })
        })
    }

    tab.setPane(
        isc.TabSet.create({
            tabs:  tabset
        })
    );
}

function showViewSystem(data, id){
    // Variables de datos
    var system = data[0];
    var modules = system.modules;

    var module_interfaces = new Array();
    for (var i =0; i<modules.length; i++) {
        if ( modules[i].interfaces != null ) {
            for (var j =0; j<modules[i].interfaces.length; j++) {
                module_interfaces.push(modules[i].interfaces[j]);
            }
        }
    }

    // Representacion
    ContentTabSet.getTab(id).setPane(
        isc.VLayout.create({
            height : "*",
            members: [ 
                isc.DetailViewer.create({
                    data: system,
                    fields : [{ value : (system.external?isc.Canvas.imgHTML( "/media/img/external-icon.gif" )+" ":"") + "Sistema "+ system.full_name, type : "header"},
                                fieldDescription, fieldReferents, fieldDocumentation]
                }),
                isc.LayoutSpacer.create({height:"10" }),
                isc.TabSet.create({
                    tabs: [ {
                        title: "Diagrama",
                        pane: isc.Diagram.create({
                            src: diagramServiceUrl+system.diagram_uri
                            })
                        }, {
                            title: "M&oacute;dulos (" + modules.length + ")", 
                            pane: isc.DetailGrid.create({
                                data : modules,
                                fields : [ fieldExternal, fieldFullName, fieldGoal ]
                            })
                        }, {
                            title: "Interfaces (" + module_interfaces.length + ")", 
                            pane: isc.DetailGridInterface.create({
                                data: module_interfaces
                            })
                        }, {
                            title: "Dependencias (" + system.dependencies.length + ")", 
                            pane: isc.DetailGridInterface.create({
                                ID: "Dependencies",
                                data: system.dependencies
                            })
                        }, {
                            title: "Dependencias desde otros sistemas (" + system.dependents.length + ")", 
                            pane: isc.DetailGridInterface.create({
                                ID: "Dependents",
                                data: system.dependents
                            })
                        }
                    ]
                })
            ]
        })
    );
}

function showViewModule( data, id ){
    var module = data[0];

    ContentTabSet.getTab(id).setPane(
        isc.VLayout.create({
            height : "*",
            members: [
                isc.DetailViewer.create({
                    data: module,
                    fields : [{ value : (module.external?isc.Canvas.imgHTML( "/media/img/external-icon.gif" )+" ":"") + "M&oacute;dulo "+ module.full_name, type : "header"},
                                fieldGoal, fieldReferents, fieldDocumentation]
                }),
                isc.LayoutSpacer.create({height:"10" }),
                isc.TabSet.create({
                    tabs: [{
                        title: "Diagrama",
                        pane: isc.Diagram.create({
                            src: diagramServiceUrl+module.diagram_uri
                            })
                        }, {
                        title: "Interfaces (" + module.interfaces.length + ")", 
                        pane: isc.DetailGridInterface.create({
                                data: module.interfaces
                        })
                    }]
                })
            ]
        })
    );
 }

function showViewInterface( data, id ){
    var interface = data[0];

    ContentTabSet.getTab(id).setPane(
        isc.VLayout.create({
            height : "*",
            members: [
                isc.DetailViewer.create({
                    fields : [{ value : (interface.direction?isc.Canvas.imgHTML( "/media/img/morocho/icon"+interface.direction+".png" )+" "+" ":"") + "Interface " + interface.full_name, type : "header"},
                                fieldGoal, fieldReferents, fieldDocumentation, fieldTechnology],
                    data : interface
                 }) ,
                isc.LayoutSpacer.create({height:"10" }),
                isc.TabSet.create({
                    tabs: [{
                        title: "Diagrama",
                        pane: isc.Diagram.create({
                            src: diagramServiceUrl+interface.diagram_uri
                        })
                    }]
                })
            ]
        })
    );
 }

function showViewDependency( data, id ){
    var dependency = data[0];
    var interface = new Array(dependency.interface);

    ContentTabSet.getTab(id).setPane(
        isc.VLayout.create({
            height : "*",
            members: [
                isc.DetailViewer.create({
                    fields : [{ value : (dependency.direction?isc.Canvas.imgHTML( "/media/img/morocho/icon"+dependency.direction+".png" )+" "+" ":"") + "Dependencia " + dependency.full_name, type : "header"},
                                fieldGoal, fieldReferents, fieldDocumentation, fieldTechnology],
                    data: dependency
                }),
                isc.LayoutSpacer.create({height:"10" }),
                isc.TabSet.create({
                    tabs: [{
                        title: "Interfaz utilizada", 
                        pane: isc.DetailGridInterface.create({
                            data: interface
                        })
                    }]
                })
            ]
        })
    );
 }

// INTERFACE
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
            imageType : "natural",
             src : "grass.png",
         }) ]
     }), isc.HLayout.create({
        ID : "ContentSection",
        height : "*",
        showEdges : "true",
        members : [ isc.TreeGrid.create({
            ID : "NavigationTree",
            width : 300,
            dataSource : isc.JsonDataSource.create({
                dataURL : "{% url api_model %}",
                fields : [ {
                    name : "name"
                 }]
            }),
            autoFetchData : true,
            dataProperties: {openProperty: "isOpen"},
            loadDataOnDemand : false,
            defaultIsFolder : false,
            showResizeBar : true,
            generateClickOnEnter : true,
            dataArrived: function ( p ) {
                openTab( null, p.children[0] );
            },
            fields : [{
                name : "name",
                recordDoubleClick : openTab
            }]
        }), isc.TabSet.create({
            ID : "ContentTabSet"
        })
        ]
     }), isc.HStack.create({
        ID : "FooterSection",
        height : "1",
        members : [ isc.IButton.create({
            title : "Console",
            click : "isc.showConsole()"
         }) ]
     }) ]
 });
