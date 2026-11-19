#!/usr/bin/env Rscript
# Scientific calculations and parameters retained from the archived native R scripts.
# Cleaned keyword input and preserved VOSviewer inputs replace workstation-specific paths.
suppressPackageStartupMessages({library(bibliometrix); library(igraph); library(jsonlite)})
script <- sub('^--file=', '', grep('^--file=', commandArgs(FALSE), value=TRUE)[1])
root <- normalizePath(file.path(dirname(script), '..'))
out <- file.path(root, 'results', 'native')
dir.create(out, recursive=TRUE, showWarnings=FALSE)
z <- fromJSON(file.path(root, 'data', 'networks.json'), simplifyVector=FALSE)
for (name in names(z$native_vosviewer_inputs)) {
  cat(z$native_vosviewer_inputs[[name]], file=file.path(out, name))
}
# Co-citation clustering/layout: full 60-reference graph, association-strength weights.
rows <- z$cocitation_matrix
labels <- names(rows[[1]])[-1]
a <- do.call(rbind, lapply(rows, function(r) as.numeric(unlist(r[labels]))))
dimnames(a) <- list(labels, labels)
occ <- diag(a); diag(a) <- 0
g <- graph_from_adjacency_matrix(a / outer(occ, occ), mode='undirected', weighted=TRUE, diag=FALSE)
set.seed(20261112)
cl <- cluster_louvain(g, weights=E(g)$weight)
set.seed(20261112)
xy <- layout_with_fr(g, weights=E(g)$weight, niter=3000)
write.csv(data.frame(name=labels, occurrences=occ, community=as.integer(membership(cl)),
                     x=xy[,1], y=xy[,2]), file.path(out, 'cocitation-nodes.csv'), row.names=FALSE)
write_json(list(seed=20261112, full_edges=ecount(g), modularity=modularity(cl),
                communities=as.integer(sizes(cl))), file.path(out, 'cocitation-summary.json'), pretty=TRUE)
# Native Bibliometrix thematic analysis, using exactly the released cleaned DE strings.
d <- read.csv(file.path(root, 'data', 'corpus.csv'), check.names=FALSE, stringsAsFactors=FALSE)
M <- data.frame(UT=d$ut, SR=d$SR, DB=d$DB, PY=d$year, DE=d$keywords_clean,
                DI=d$doi, AU=d$AU, TI=d$TI, SO=d$SO, TC=d$global_citations,
                stringsAsFactors=FALSE)
periods <- list('2006-2010'=c(2006,2010), '2011-2015'=c(2011,2015),
                '2016-2020'=c(2016,2020), '2021-2025'=c(2021,2025))
for (name in names(periods)) {
  yy <- periods[[name]]
  s <- M[M$PY >= yy[1] & M$PY <= yy[2], , drop=FALSE]
  tm <- thematicMap(s, field='DE', n=100, minfreq=if(nrow(s)<100) 2 else 5, seed=1234)
  saveRDS(tm, file.path(out, paste0('thematic-map-', name, '.rds')))
  if (!is.null(tm$map)) {
    ggplot2::ggsave(file.path(out, paste0('thematic-map-', name, '.pdf')), tm$map, width=7, height=5)
  }
}
te <- thematicEvolution(M, field='DE', years=c(2010,2015,2020), n=100, minFreq=2, seed=1234)
saveRDS(te, file.path(out, 'thematic-evolution.rds'))
write.csv(te$Nodes, file.path(out, 'thematic-evolution-nodes.csv'), row.names=FALSE)
write.csv(te$Edges, file.path(out, 'thematic-evolution-edges.csv'), row.names=FALSE)
writeLines(capture.output(sessionInfo()), file.path(out, 'session-info.txt'))
cat('Native calculations completed. VOSviewer map/network inputs exported to ', out, '\n', sep='')
