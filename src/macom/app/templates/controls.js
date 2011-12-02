isc.defineClass("DetailGrid", "ListGrid").addProperties({
  alternateRecordStyles : true,
  autoFetchData : true,
  showFilterEditor : true,
  filterOnKeypress : true
});

isc.defineClass("JSONDataSource", "DataSource").addProperties({
  dataFormat : "json",
  dataProtocol : "getParams"
});

isc.defineClass("Diagram", "VLayout").addProperties({
  height : "*",
  diagramRenderServiceURL : "{{diagram_service_url}}/",
  initWidget : function() {
    this.diagramSourceURL = window.location.protocol + "//" + window.location.host + this.src;
    this.diagramImageURL = this.diagramRenderServiceURL + this.diagramSourceURL;
    this.diagramSourceButton = isc.IButton.create({
      title : "View source",
      diagramSourceURL : this.diagramSourceURL,
      click : function() {
        mcm.showSource("Diagram Source", this.diagramSourceURL);
      }
    });
    this.diagramContainer = isc.HStack.create();
    this.addMembers([ this.diagramContainer, this.diagramSourceButton ]);
    var image = new Image();
    image.diagram = this;
    image.onload = function() {
      this.diagram.diagramImage = isc.Img.create({
        imageType : "normal",
        width : this.width,
        height : this.height,
        src : this.src
      });
      this.diagram.diagramContainer.addMember(this.diagram.diagramImage);
    }
    image.src = this.diagramImageURL;
    return this.Super("initWidget", arguments);
  }
});

isc.defineClass("ItemViewer", "VLayout").addProperties({
    title : false,
    data : false, // Datos a mostrar del item
    fields : false, // Definicion de los fields de la informacion del item
    additionalInfo : false,
    height : "*",
    initWidget : function() {
        // Detalles del Item
        var infoFields = new Array();
        // titulo
        
        infoFields.push({
          value : (this.title ? this.title + " " : "") + this.data.full_name + new mcm.IconsFactory(this.data).getAllIcons(),
          type : "header"
        });
        if (this.fields) {
            infoFields = infoFields.concat(this.fields); // Definicion de datos
        }
        this.detail = isc.DetailViewer.create({
          autoFetchData : true,
          fields : infoFields,
          data : this.data
        });
        // Spacer
        this.spacer = isc.LayoutSpacer.create({
          height : "10"
        });
        // Tabs de informacion
        var tabsInfo = new Array();
        if (this.data.diagram_uri) {
          tabsInfo.push({
            title : "Diagrama",
            pane : isc.Diagram.create({
              ID : this.data.full_name + "_" + this.ID,
              src : this.data.diagram_uri
            })
          });
        }
        if (this.additionalInfo) {
            tabsInfo = tabsInfo.concat(this.additionalInfo);
        }
        this.tabs = isc.TabSet.create({
          tabs : tabsInfo
        });
        this.addMembers([ this.detail, this.spacer, this.tabs ]);
        
        return this.Super("initWidget", arguments);
    }
});

isc.defineClass("SourceViewer", "Window").addProperties({
  autoCenter : true,
  isModal : true,
  showModalMask : true,
  showMinimizeButton : false,
  width : "90%",
  height : "90%",
  items : isc.Layout.create({
    hPolicy : "fill",
    vPolicy : "fill",
    members : isc.HTMLPane.create({
      contentsType : "page"
    })
  }),
  initWidget : function() {
    this.items.members[0].setContentsURL(this.sourceURL);
    return this.Super("initWidget", arguments);
  }
});

mcm.showSource = function(title, sourceURL) {
  isc.SourceViewer.create({
    title : title,
    sourceURL : sourceURL
  })
}

// constantes de dirección
mcm.direction = {
	IN : "in",
	OUT : "out",
	INOUT : "in-out"
}

mcm.IconsFactory = function (node){
	this.iconPreffix = "/media/img/";
	this.spacer = " ";
	this.node = node;
	this.icons = {};
	this.showLabels = true;

	this.toHTMLLabel = function( label ) {
		if ( this.showLabels && label ){
			return this.spacer + "<span style='font-size: 10px !important'>" + label + "</span>"; 
		} else return "";
	}
	
	this.toHTMLIcon = function( src, label, tooltip, w, h){
		if (!w) w=16; if (!h) h=16;
		return isc.Canvas.imgHTML(this.iconPreffix + src, w, h, null, ( tooltip?"title=\"" + tooltip + "\"":"")) + this.toHTMLLabel(label);		
	};
	
	this.icon = {
		error : this.toHTMLIcon("error.png", "Sin datos", "Sin datos cargados")
	}
	
	this.addIcon = function ( id, icon, tooltip, label, container, w, h){
		if (!container) container = this.icons;

		container[id] = this.toHTMLIcon( icon, label, tooltip, w, h);
	}
	
	var title = "";
	
	if ( this.node.kind ) {
		var tooltip = "";

		switch (this.node.kind){
			case "root": title = "Sistema"; break;
			case "system": title = "Sistema"; break;
			case "module": title = "Módulo"; break;
			case "interface": title = "Interfáz"; break;
			case "dependency": title = "Dependencia"; break;
		}
		
		if ( this.node.external ){
			tooltip += " externo";
		}
		this.addIcon( "kind", this.node.kind + (this.node.external ? "-external" : "") + ".png", title + " " + tooltip, null );
	};

	if ( this.node.external ){
		this.addIcon( "external", "external-icon.gif", title + " externo", "externo");
	}
	
	if ( this.node.direction != undefined ) {
		if ( this.node.direction && this.node.direction == mcm.direction.IN || this.node.direction == mcm.direction.INOUT ){
			this.addIcon( "direction-in", "iconin.png", "Flujo de información entrante", "entrada" );
		}
		
		if ( this.node.direction && this.node.direction == mcm.direction.OUT || this.node.direction == mcm.direction.INOUT ){	
			this.addIcon( "direction-out", "iconout.png", "Flujo de información saliente", "salida" );
		}
	};
	
	this.getNodeIcon = function (){
		// todo: definir icono de kind detault
		return this.getIcon('kind');
	};

	this.getIcon = function (id){
		if ( id && this.icons[id]) return this.icons[id];
		else return "";
	};
	
	this.getAllIcons = function (){
		var iconsHTML = "";
		for ( i in this.icons ){
			if ( i != "kind") { // Solo el kind es un icono especial, por eso se excluye
				iconsHTML += this.spacer + this.icons[i];
			}
		}

		return iconsHTML; 
	};
}
