// Fields Predefinidos
var fieldFullName = { name : "full_name", title : "Nombre" };
var fieldDescription = { name : "description", title : "Descripci&oacute;n" };
var fieldGoal = { name : "goal", title : "Objetivo" };
var fieldReferents = { name : "referents", title : "Referentes" };
var fieldDocumentation = { name : "documentation", title : "Documentaci&oacute;n" };
var fieldTechnology = { name : "technology", title : "Tecnolog&iacute;a", width: "100" };
var fieldDirection = { name : "direction", title : " ", width: "20", type:"image", imageURLPrefix:"/media/img/icon", imageURLSuffix:".png" };
var fieldExternal = { name : "external", title : " ", width: "20", type:"image", imageURLPrefix:"/media/img/external", imageURLSuffix:"-icon.gif" };

// Propiedades default en objetos de SmartClient
isc.defineClass("Diagram", "VLayout").addProperties({
    height: "*",
    initWidget: function () {
        this.diagramImage = isc.Img.create({
            src: "{{diagram_service_url}}/"+window.location.protocol+"//"+window.location.host + this.src,
            imageType: "normal",
            height: "*",
            cursor: "pointer",
            click : function(){
                window.open ( this.src );
            }
        });

        setDelayImgSize("{{diagram_service_url}}/"+window.location.protocol+"//"+window.location.host + this.src, this.diagramImage.ID);

        this.sourceButton = isc.IButton.create({
            title: "Source",
            diagramSrc: this.src,
            top: 35,
            left: 75,
            click : function () {
                modalWindow.setTitle("Source");
                modalWindow.show();
                modalWindowPane.setContentsURL( window.location.protocol+"//"+window.location.host + this.diagramSrc );
                modalWindowPane.setHeight(modalWindow.getHeight()); //Fix, no me funciona bien el alto
            }
        });

        this.addMembers([this.diagramImage, this.sourceButton]);
        
        return this.Super("initWidget", arguments);
    }
});
// Esta funcion espera que este las dimenciones de la imagen y la impacta en el control de imp
// Se genero el wirkarround para chromium por tener un gran delay en las dimenciones de la imagen y no poner correctamente las barras de scroll
function setDelayImgSize(imgSrc, obj, iteration) {
    if ( !iteration) iteration = 0;
    
    var img = new Image();
    img.src = imgSrc;
    
    if ( img.width == 0 )
        if ( iteration < 5 ) window.setTimeout('setDelayImgSize("'+ imgSrc + '","' + obj + '")', 100, iteration++);
    else {
        var o = eval(obj);
        o.imageWidth = img.width;
        o.imageHeight = img.height;
        o.resetSrc();
        o.redraw();
    }
}

isc.Window.create({
    ID: "modalWindow",
    autoSize: true,
    autoCenter: true,
    width: "95%",
    height: "95%",
    isModal: true,
    showModalMask: true,
    autoDraw: false,
    showMinimizeButton: false,
    items: isc.HTMLPane.create({
        ID:"modalWindowPane",
        width: "100%",
        height: "100%",
        contentsType:"page"
    })
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

isc.defineClass("DetailGridDependency", "DetailGrid").addProperties({
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
            title : isc.Canvas.imgHTML(getIconByKind(record)) +"  "+ ( record.full_name.length > 40 ? "... " + record.full_name.substring(record.full_name.length - 40) : record.full_name ),
            record : record
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
                src: record.diagrams[i].diagram_uri
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
                    fields : [{ value : "Sistema "+ system.full_name + (system.external?" "+isc.Canvas.imgHTML( "/media/img/external-icon.gif" ):""), type : "header"},
                                fieldDescription, fieldReferents, fieldDocumentation]
                }),
                isc.LayoutSpacer.create({height:"10" }),
                isc.TabSet.create({
                    tabs: [ {
                        title: "Diagrama",
                        pane: isc.Diagram.create({
                            src: system.diagram_uri
                            })
                        }, {
                            title: "M&oacute;dulos (" + modules.length + ")", 
                            pane: isc.DetailGrid.create({
                                ID: "systemModules" + system.full_name,
                                data : modules,
                                fields : [ fieldExternal, fieldFullName, fieldGoal ]
                            })
                        }, {
                            title: "Interfaces (" + module_interfaces.length + ")", 
                            pane: isc.DetailGridInterface.create({
                                 ID: "systemInterfaces" + system.full_name,
                                data: module_interfaces
                            })
                        }, {
                            title: "Dependencias (" + system.dependencies.length + ")", 
                            pane: isc.DetailGridDependency.create({
                                ID: "systemDependencies" + system.full_name,
                                data: system.dependencies
                            })
                        }, {
                            title: "Dependencias desde otros sistemas (" + system.dependents.length + ")", 
                            pane: isc.DetailGridDependency.create({
                                ID: "systemDependents" + system.full_name,
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
                    fields : [{ value : "M&oacute;dulo "+ module.full_name + (module.external?" "+isc.Canvas.imgHTML( "/media/img/external-icon.gif" ):""), type : "header"},
                                fieldGoal, fieldReferents, fieldDocumentation]
                }),
                isc.LayoutSpacer.create({height:"10" }),
                isc.TabSet.create({
                    tabs: [{
                        title: "Diagrama",
                        pane: isc.Diagram.create({
                            ID: "moduleDiagram" + module.full_name,
                            src: module.diagram_uri
                        })
                    }, {
                        title: "Interfaces (" + module.interfaces.length + ")", 
                        pane: isc.DetailGridInterface.create({
                            ID: "moduleInterfaces" + module.full_name,
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
                    fields : [{ value : "Interface " + interface.full_name + (interface.direction?" "+isc.Canvas.imgHTML( "/media/img/icon"+interface.direction+".png" )+" ":""), type : "header"},
                                fieldGoal, fieldReferents, fieldDocumentation, fieldTechnology],
                    data : interface
                 }) ,
                isc.LayoutSpacer.create({height:"10" }),
                isc.TabSet.create({
                    tabs: [{
                        title: "Diagrama",
                        pane: isc.Diagram.create({
                            ID: "interfaceDiagram" + interface.full_name,
                            src: interface.diagram_uri
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
                    fields : [{ value : "Dependencia " + dependency.full_name + (dependency.direction?" "+isc.Canvas.imgHTML( "/media/img/icon"+dependency.direction+".png" )+" ":""), type : "header"},
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

function getIconByKind( node ){
    return "/media/img/" + node.kind + ( node.external?"-external":"") + ".png";
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
            getIcon: function (node){
                    return "/media/img/" + node.kind + ".png";
            },
            width : 300,
            dataSource : isc.JsonDataSource.create({
                dataURL : "{% url api_model %}",
                fields : [
                    { name : "name", title: "Sistemas" },
                 ]
            }),
            autoFetchData : true,
            dataProperties: {openProperty: "isOpen"},
            loadDataOnDemand : false,
            defaultIsFolder : false,
            showResizeBar : true,
            generateClickOnEnter : true,
            getIcon: function (node){
                return getIconByKind(node);
            },
            dataSource : isc.JsonDataSource.create({
                dataURL : "{% url api_model %}",
                fields : [ {
                    name : "name"
                 }]
            }),
            dataArrived: function ( p ) {
                openTab( null, p.children[0] );
            },
            fields : [{
                name : "name",
                recordDoubleClick : openTab
            }],
            recordDoubleClick : function(){} // Elimina el evento de dobleClick por default
        }), isc.TabSet.create({
            ID : "ContentTabSet",
            canCloseTabs : true,
            closeTabIconSize: 12
        })]
    })]
 });
 
 
