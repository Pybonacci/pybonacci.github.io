---
title: Como hacer un mapa muy bonito de España en ggplot2
date: 2017-04-17T08:57:12+00:00
author: Manuel Garrido
slug: como-hacer-un-mapa-muy-bonito-de-espana-en-ggplot2
tags: gis, mapa, mapping, opendata, R

_(Este post apareció originalmente en <a href="http://blog.manugarri.com/making-a-beautiful-map-of-spain-in-ggplot2/" target="_blank">mi blog</a>)._

Hace unas semanas leí un artículo en el cual Timo Grossenbacher mostraba como consiguió hacer, en mi opinión, <a href="https://timogrossenbacher.ch/2016/12/beautiful-thematic-maps-with-ggplot2-only/" target="_blank">uno de los mapas más bonitos que he visto nunca</a>. Timo empleó la que es, en mi opinión, una de las librerias más expresivas y bellas que hay para hacer gráficos, <a href="http://ggplot2.org/" target="_blank">ggplot2</a>. La versión original de ggplot2 es para R, pero existe una versión de python no exhaustiva gracias a la buena gente de <a href="http://ggplot.yhathq.com/" target="_blank">Yhat</a>.

Asi que por supuesto, tenía que replicarlo.

Antes que nada, aquí está el mapa.

![Mapilla](http://i.imgur.com/MrNL3bE.png)

El código empleado para hacer el mapa lo podeis descargar en <a href="https://github.com/manugarri/spain_census_map" target="_blank">github</a>. He compartido varias versiones del mapa para que se pueda observar como los diferentes cambios en las escalas afectan a la visualización.

#Código.

Para empezar, importamos las librerías necesarias:

<pre class=" language-r"><code class=" language-r">
setwd("/DIRECTORIO_DE_TRABAJO/")

if (!require(rgdal)) {
install.packages("rgdal", repos = "http://cran.us.r-project.org")
require(rgdal)
}

if (!require(rgeos)) {
install.packages("rgeos", repos = "http://cran.us.r-project.org")
require(rgeos)
}
if (!require(rgdal)) {
install.packages("rgdal", repos = "http://cran.us.r-project.org")
require(rgdal)
}
if (!require(raster)) {
install.packages("raster", repos = "http://cran.us.r-project.org")
require(raster)
}
if(!require(ggplot2)) {
install.packages("ggplot2", repos="http://cloud.r-project.org")
require(ggplot2)
}
if(!require(viridis)) {
install.packages("viridis", repos="http://cloud.r-project.org")
require(viridis)
}
if(!require(dplyr)) {
install.packages("dplyr", repos = "https://cloud.r-project.org/")
require(dplyr)
}
if(!require(gtable)) {
install.packages("gtable", repos = "https://cloud.r-project.org/")
require(gtable)
}
if(!require(grid)) {
install.packages("grid", repos = "https://cloud.r-project.org/")
require(grid)
}
if(!require(tidyr)) {
install.packages("tidyr", repos = "https://cloud.r-project.org/")
require(tidyr)
}
}
 </code></pre>

El siguiente paso es importar los datos. Tras mucho buscar, encontré un archivo shapefile con los municipios españoles en <a href="http://www.arcgis.com/home/item.html?id=2e47bb12686d4b4b9d4c179c75d4eb78" target="_blank">ArcGis</a>, sin ninguna atribución que pudiera encontrar.

Para obtener los datos del censo español, hice uso de la \*fantástica\* herramienta de <a href="http://www.ine.es/censos2011_datos/cen11_datos_detallados.htm" target="_blank">extracción de datos</a> proporcionada por el Instituto Nacional de Estadística. La herramienta es una pesadilla en términos de usabilidad, así que si queréis simplemente hacer el mapa he compartido los datos en el repositorio.

<pre class=" language-r"><code class=" language-r">
data_spain data_spain$municipality_code data_spain$People data_spain$Average.age

#Cargamos el shapefile y lo convertimos en un dataframe
municipalities_spain map_data_fortified_spain % mutate(id = as.numeric(id))

#Ahora unimos los datos del censo con los datos geométricos usando municipality_code como clave
map_data_spain % left_join(data_spain, by = c("id" = "municipality_code")) %&gt;% fill(Average.age)
rm(data_spain)
rm(map_data_fortified_spain)
rm(municipalities_spain)
 </code></pre>

Finalmente, el código para hacer el mapa en sí. Hay muchísima lógica en dicho código orientada a hacer el mapa más bonito, os recomiendo mirar el artículo original para ver la evolución de los parámetros del gráfico, en particular todo lo relativo a la escala de colores.

<pre class=" language-r"><code class=" language-r">
# Aquí hacemos que los saltos de la escala de edades sean más bonitos e informativos visualmente

# encontramos los extremos del rango de edad
minVal maxVal # calculamos los valores de las etiquetas de los rangos de edad
labels brks # Redondeamos los extremos del rango de edad
for(idx in 1:length(brks)){
labels }

labels # definimos una nueva variable con los datos de la escala de edad
map_data_spain$brks breaks = brks,
include.lowest = TRUE,
labels = labels)

brks_scale labels_scale

theme_map theme_minimal() +
theme(
text = element_text(family = "Ubuntu Regular", color = "#22211d"),
axis.line = element_blank(),
axis.text.x = element_blank(),
axis.text.y = element_blank(),
axis.ticks = element_blank(),
axis.title.x = element_blank(),
axis.title.y = element_blank(),
# panel.grid.minor = element_line(color = "#ebebe5", size = 0.2),
panel.grid.major = element_line(color = "#ebebe5", size = 0.2),
panel.grid.minor = element_blank(),
plot.background = element_rect(fill = "#f5f5f2", color = NA),
panel.background = element_rect(fill = "#f5f5f2", color = NA),
legend.background = element_rect(fill = "#f5f5f2", color = NA),
panel.border = element_blank(),
...
)
}

#Esta función simplemente extiende los extremos de la escala de edad para llegar al mínimo y el máximo
extendLegendWithExtremes p_grob legend legend_grobs # grab the first key of legend
legend_first_key legend_first_key$widths # modify its width and x properties to make it longer
legend_first_key$grobs[[1]]$width legend_first_key$grobs[[1]]$x

# último valor de la leyenda
legend_last_key legend_last_key$widths

legend_last_key$grobs[[1]]$width legend_last_key$grobs[[1]]$x

# cambiamos también la posición de la última etiqueta para que no se superponga a la anterior
legend_last_label legend_last_label$grobs[[1]]$x

# Insertamos el nuevo color de la leyenda en la leyenda combinada
legend_grobs$grobs[legend_grobs$layout$name == "key-3-1-1"][[1]] &lt;-
legend_first_key$grobs[[1]]
legend_grobs$grobs[legend_grobs$layout$name == "key-3-6-1"][[1]] &lt;-
legend_last_key$grobs[[1]]
legend_grobs$grobs[legend_grobs$layout$name == "label-5-6"][[1]] &lt;-
legend_last_label$grobs[[1]]

# Ahora lo mismo para el valor mínimo de la leyenda
new_first_label new_first_label$label new_first_label$x new_first_label$hjust

legend_grobs new_first_label,
t = 6,
l = 2,
name = "label-5-0",
clip = "off")
legend$grobs[[1]]$grobs[1][[1]] p_grob$grobs[p_grob$layout$name == "guide-box"][[1]]

# se usa esta función para dibujar la escala
grid.newpage()
grid.draw(p_grob)
}

p geom_polygon(data = map_data_spain, aes(fill = brks,
x = long,
y = lat,
group = group)) +
# municipality outline
geom_path(data = map_data_spain, aes(x = long,
y = lat,
group = group),
color = "white", size = 0.1) +
coord_equal() +
theme_map() +
theme(
legend.position = c(0.7, 0.03),
legend.text.align = 0,
legend.background = element_rect(fill = alpha('white', 0.0)),
legend.text = element_text(size = 14, hjust = 0, color = "#4e4d47"),
legend.title = element_text(size = 20),
plot.title = element_text(size = 28, hjust = 0.8, color = "#4e4d47"),
plot.subtitle = element_text(size = 20, hjust = 0.8, face = "italic", color = "#4e4d47"),
plot.caption = element_text(size = 14, hjust = 0.95, color = "#4e4d47"),
plot.margin = unit(c(.5,.5,.2,.5), "cm"),
panel.border = element_blank()
) +
labs(x = NULL,
y = NULL,
title = "Spain's regional demographics",
subtitle = "Average age in Spanish municipalities, 2011",
caption = "Author: Manuel Garrido (@manugarri) Original Idea: Timo Grossenbacher (@grssnbchr), Geometries: ArcGis Data: INE, 2011;") +
scale_fill_manual(
values = rev(magma(8, alpha = 0.8)[2:7]),
breaks = rev(brks_scale),
name = "Average age",
drop = FALSE,
labels = labels_scale,
guide = guide_legend(
direction = "horizontal",
keyheight = unit(2, units = "mm"),
keywidth = unit(70/length(labels), units = "mm"),
title.position = 'top',
title.hjust = 0.5,
label.hjust = 1,
nrow = 1,
byrow = T,
reverse = T,
label.position = "bottom"
)
)
extendLegendWithExtremes(p)
 </code></pre>

Este código está diseñado muy cuidadosamente para exportar una imagen con un ancho de 2400 píxeles.

Dado que las islas Canarias estan muy alejadas de la península, una práctica común es desplazar las islas más cerca de España, esto lo he hecho en Gimp.

#Notas.

- Yo sabía que España tenía un problema poblacional, pero ¡madre mía! El noroeste del pais parece un gran asilo. El mapa original de Suiza tenia una escala de edad en el rango 40-52 años, pero he tenido que expandirlo a 40-56 debido al envejecimiento poblacional español.

- Una vez más, me he dado cuenta de lo mal que está el movimiento Open Data en España:

  * La herramienta de extracción de datos del INE parece que se hizo en los años 90 (tanto en usabilidad como en velocidad).
  * La información del censo de España se actualiza, ¡cada 10 años!. Esto significa que este mapa está usando la información más actualizada que existe de la población española, y es de 2011. Estos datos deberían actualizarse más frecuentemente en un mundo en el que todo cambia más rápido.
  * Si vais al mapa del artículo original, vereis que su mapa tiene una capa de topografía muy bonita encima de los municipios. Timo usó una imagen ráster a escala 1:1.000.000 con información topográfica proporcionada por la oficina federal de topografía suiza.
  
    Yo me tiré un dia entero buscando algo similar para España, y según parece el Centro Nacional de Información Geográfica sólo proporciona mapas ráster <a href="http://centrodedescargas.cnig.es/CentroDescargas/buscadorCatalogo.do" target="_blank">en la escala de 25 y 50 metros</a> lo que obliga a descargarte cientos de archivos de imagen y unirlos luego. De verdad que yo no tenía ganas de hacer eso para hacer un mapa a escala tan pequeña. Al final, me hice mi propia imágen topográfica raster tomando imágenes de internet que procesé en Gimp. No incluyo el relieve en el mapa por que, al contrario que con Suiza (donde no hay municipios en la región de los Alpes), en España mostrar el relieve ocultaría la información de los municipios por debajo.

- Aunque tengo que decir que la cantidad de esfuerzo y dedicación que ha llevado realizar este mapa es impresionante (una de las principales razones por las cuales yo quería replicarlo), creo que debería haber una manera mejor de hacer gráficas customizadas en ggplot2. El código actual solo funciona con una resolución específica en mente, y se necesitan un montón de pruebas hasta llegar a encontrar los tamaños de fuentes que hacen que todo encaje. Idealmente ggplot2 usaría un sistema de referencia variable (algo como los _em_ en css) que cambiara en funcion del tamaño del mapa.

Eso es todo por hoy, muchas gracias por vuestra atención 🙂
