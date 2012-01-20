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

isc.defineClass("TagCloud", "HTMLPane").addProperties({
	height : "100%",
	width : "100%",
	resource_uri : "",
	maxFontSizeDelta: 5,
	maxtags: 100, // numero maximo de items a mostrar en la nuve
	styleName :"tagCloud",
	opener: "",
	initWidget : function() {
		//Calcular contenidos
		var self = this;
	
		isc.JSONDataSource.create({
            dataURL : this.resource_uri
        }).fetchData( null, function (data) {
        	var dt = data.data;
        	if ( dt && dt.length > 0){
	        	var html = "";

	        	// Recortar el array de datos a los "this.maxtags" y
	        	// Ordenar tags resultantes alfabeticamente
	        	var d  = dt.slice(0, self.maxtags).sort(function(a, b){
	        		 var nameA=a.name.toLowerCase(), nameB=b.name.toLowerCase()
	        		 if (nameA < nameB) //sort string ascending
	        		  return -1
	        		 if (nameA > nameB)
	        		  return 1
	        		 return 0 //default return value (no sorting)
	        		}
	        	);
	        	
	        	counts = mcm.util.map(function(tag) { return tag.count }, d);
				mincount = mcm.util.min(counts);
				amplitude = mcm.util.max(counts) - mincount;
				scale = 2 * self.maxFontSizeDelta / amplitude;

	        	for ( var i =0; i < d.length; i++ ){
	        		var t = d[i];
	        		var size = ((t.count - mincount) * scale - self.maxFontSizeDelta);
	        		html += mcm.util.sprintf('<a href="#" onclick=\'mcm.showTag("%s","%s","%s")\'><font size="%s">%s</font></a> ', t.name, t.resource_uri, self.opener, (size>0?"+":"")+size, t.name)
	        	}
	        	self.contents = html;
        	}
        });
		return this.Super("initWidget", arguments);
	}
});

isc.defineClass("TagDetailViewer", "Window").addProperties({
  autoCenter : true,
  title: "Etiqueta",
  isModal : true,
  showModalMask : true,
  showMinimizeButton : false,
  showHeaderIcon: false,
  resource_uri : "",
  width : "90%",
  height : "90%",
  items : isc.VLayout.create({
	  hPolicy : "fill",
	  vPolicy : "fill",
	  layoutMargin: 5
  }),
  opener : null, // Funcion de apertura de tabs
  initWidget : function() {
	  var self = this;
	  
	  var title = isc.Label.create({
		  styleName: "windowTitle",
		  contents: self.title,
		  height: "25px"
	  });
	  
	  var desc = isc.Label.create({
		  styleName: "windowDescription",
		  contents: "Lista de items relacionados con la etiqueta seleccionada",
		  height: "15px"
	  });
	  
	  var ds = isc.JSONDataSource.create({
		  dataURL : this.resource_uri,
		  autoFetchData : true,
		  fields: [ mcm.fields.KindIcon, mcm.fields.Kind, mcm.fields.FullName, mcm.fields.DescriptionAndGoal ]
	  });
	  
	  if (this.items.members && this.items.members.length > 0){
		  this.items.removeMembers(this.items.getMembers()); 
	  }
	  
	  var grid = isc.ListGrid.create({
		  alternateRecordStyles : true,
		  recordDoubleClick: function (viewer, record, recordNum, field, fieldNum, value, rawValue) {
			  self.opener(viewer, record, recordNum, field, fieldNum, value, rawValue);
			  self.closeClick();
		  }
	  });
	  
	  this.items.addMembers([title, desc, grid]);
	  grid.setDataSource(ds);
	  grid.fetchData();

	  return this.Super("initWidget", arguments);
  }
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
	height : "100%",
	title : false,
    data : false, // Datos a mostrar del item
    fields : false, // Definicion de los fields de la informacion del item
    opener: null,
    additionalInfo : false,
    height : "*",
    formatTitleValue: function (data) {
    	if ( data.full_name ){
    		return data.full_name; 
    	} else {
    		return data.name;
    	}
    },
    getOpenerLink : function (title, obj){
    	return isc.Canvas.linkHTML("javascript:" + this.opener + "(null," + 
    			"{" +
    				"kind:\"" + obj.kind + "\"," +
    				"name:\"" + obj.name + "\"," +
    				"resource_uri:\"" + obj.resource_uri + "\""+
    			"}" +
    	")", title + " " + obj.name );
    },
    initWidget : function() {
    	
    	// Breadcrumb
    	if (this.data.kind != null || typeof (this.data.kind) != 'undefined') {
    		var bcHTML = "";
    		switch (this.data.kind){
	    	case "system":
	    		// bcHTML = "" // NADA
	    		break;
			case "module":
				bcHTML = this.getOpenerLink( "Sistema", this.data.system );
				break;
			case "interface":
				bcHTML = this.getOpenerLink( "Sistema", this.data.module.system ) + "&nbsp;:&nbsp;" +
						 this.getOpenerLink( "Módulo", this.data.module );
				break;
			case "dependency":
				bcHTML = this.getOpenerLink( "Sistema", this.data.interface.module.system ) + "&nbsp;:&nbsp;" +
						 this.getOpenerLink( "Módulo", this.data.interface.module ) + "&nbsp;:&nbsp;" +
						 this.getOpenerLink( "Interface", this.data.interface );
				break;
	    	}

    		if ( bcHTML.length > 0 ) {
	        	this.breadcrumb = isc.HTMLFlow.create({
	        	    width:"100%",
	        	    height: "10px",
	        	    className: "breadcrumb",
	        	    contents: bcHTML
	        	});
    		}
    	}
    	
    	// Detalles del Item
        var infoFields = new Array();

        // titulo
        var headerTitle = isc.Label.create ( { 
        	className: "detailHeader",
        	height: "25px",
        	contents: (this.title ? this.title + " " : "") +
        			  this.formatTitleValue(this.data) +
        	  		  new mcm.IconsFactory(this.data).getAll() });

        if (this.fields) {
            infoFields = infoFields.concat(this.fields); // Definicion de datos
        }
        this.detail = isc.DetailViewer.create({
          height: "1px",
          autoFetchData : true,
          fields : infoFields,
          data : this.data
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
        
        this.addMembers([ this.breadcrumb,
                          isc.LayoutSpacer.create({ height : "5" }),
                          headerTitle,
                          isc.LayoutSpacer.create({ height : "5" }),
                          this.detail,
                          isc.LayoutSpacer.create({ height : "10" }),
                          this.tabs ]); 
        
        return this.Super("initWidget", arguments);
    }
});

isc.defineClass("SourceViewer", "Window").addProperties({
  autoCenter : true,
  isModal : true,
  showModalMask : true,
  showMinimizeButton : false,
  showHeaderIcon: false,
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
};

mcm.showTag = function(name, resource_uri, opener) {
	isc.TagDetailViewer.create ({
		opener: eval(opener),
		title: "Etiqueta " + name, 
		resource_uri : resource_uri
	})
};

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

	this._toHTMLLabel = function( label ) {
		if ( this.showLabels && label ){
			return this.spacer + "<span class='iconlabel'>" + label + "</span>"; 
		} else return "";
	}
	
	// convert icon to html
	this._toHTML = function( icon ){
		var html = isc.Canvas.imgHTML(this.iconPreffix + icon.src, icon.width, icon.height, null, ( icon.tooltip?"title=\"" + icon.tooltip + "\"":"")) + this._toHTMLLabel(icon.label);
		if ( icon.href ) {
			return isc.Canvas.linkHTML(icon.href, html );
		} else return html;
	};
	
	this.standaricon = {
		error : this._toHTML({ src: "error.png", label: "Sin datos", tooltip: "Sin datos cargados"} )
	}
	
	this.add = function ( id, src, tooltip, label, container, w, h){
		if (!container) container = this.icons;
		if (!w) w=16; if (!h) h=16;

		container[id] = {src: src, label: label, tooltip: tooltip, width: w, height:h};
	}

	this.addAction = function ( id, src, href, tooltip, label, container, w, h){
		if (!container) container = this.icons;
		if (!w) w=16; if (!h) h=16;
		
		container[id] = {href: href, src: src, label: label, tooltip: tooltip, width: w, height: h};
	}
	
	var title = "";
	
	if ( this.node.kind ) {
		var tooltip = "";

		switch (this.node.kind){
			case "rootsystem": title = "Sistema"; break;
			case "rootpattern": title = "Patrón"; break;
			case "system": title = "Sistema"; break;
			case "module": title = "Módulo"; break;
			case "interface": title = "Interfáz"; break;
			case "dependency": title = "Dependencia"; break;
		}
		
		if ( this.node.external ){
			tooltip += " externo";
		}
		this.add( "kind", this.node.kind + (this.node.external ? "-external" : "") + ".png", title + " " + tooltip, null );
	};

	if ( this.node.external ){
		this.add( "external", "external-icon.gif", title + " externo", "externo");
	}
	
	if ( this.node.direction != undefined ) {
		if ( this.node.direction && this.node.direction == mcm.direction.IN || this.node.direction == mcm.direction.INOUT ){
			this.add( "direction-in", "iconin.png", "Flujo de información entrante", "entrada" );
		}
		
		if ( this.node.direction && this.node.direction == mcm.direction.OUT || this.node.direction == mcm.direction.INOUT ){	
			this.add( "direction-out", "iconout.png", "Flujo de información saliente", "salida" );
		}
	};
	
	if ( this.node.edit_url ){
		this.addAction( "edit_url", "edit.png", this.node.edit_url, "Editar", "editar")
	}

	if ( this.node.history_url ){
		this.addAction( "history_url", "history.png", this.node.history_url, "Historial", "historial")
	}
	
	this.getNodeIcon = function (){
		// todo: definir icono de kind detault
		return this.get('kind');
	};

	this.get = function (id){
		if ( id && this.icons[id]){
			return this._toHTML( this.icons[id] );
		} else return "";
	};
	
	this.getAll = function (){
		var html = "";
		for ( id in this.icons ){
			if ( id != "kind") { // Solo el kind es un icono especial, por eso se excluye
				html += this.spacer + this._toHTML(this.icons[id]);
			}
		}

		return html; 
	};
}
