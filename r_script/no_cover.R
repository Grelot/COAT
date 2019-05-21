#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
no_cover_file = args[1]
depth_at_each_pos_file = args[2]
coverage_threshold = as.numeric(args[3])
chr = args[4]
start = as.numeric(args[5])
end = as.numeric(args[6])

utr_start = as.numeric(args[7])
utr_end = as.numeric(args[8])

title_plot = args[9]
results_path = args[10]

#print(results_path)
no_cover = read.table(no_cover_file,header=T)
depth = read.table(depth_at_each_pos_file)
#print(no_cover)
#print(as.vector(no_cover$start))
#print(no_cover$end)
#print(start)
#print(end)
#print(utr_start)
#print(utr_end)

#print(length(depth$V3))
#print(length(start:end))
max_depth=max(depth$V3)

ylab_text = "depth"
xlab_text = paste(chr," base position")


#pdf_file=strsplit(no_cover_file, ".", fixed = TRUE)
#pdf_file=toString(pdf_file[[1]][1])
#pdf_file=paste(pdf_file,"pdf",sep=".")
#pdf_file=toString(pdf_file)
#pdf_file=paste(results_path,pdf_file,sep="/")
pdf_file=results_path
pdf_file=toString(pdf_file)
#print(pdf_file)
pdf(pdf_file, width = 12, height = 4)
par(bg = "white", fg = "black", oma = c(1,1,1,1))
plot(x=0,y=0,xlim=c(start,end),ylim=c(0,max_depth), type ="n",
bty="n",axes=F,xaxs="i",yaxs="i",xlab=xlab_text,ylab=ylab_text)
lines(start:end,depth$V3)
axis(side=1,at=seq(start,end,by=1),tcl=-0.3,labels=F,lwd=1.3,outer=F)
axis(side=2,at=seq(0,max_depth,by=5),tcl=-0.7,font=1.3,lwd=1.3,outer =F)
axis(side=2,at=seq(0,max_depth,by=1),tcl=-0.3,labels=F,lwd=1.3,outer =F)
axis(side=3,at=seq(start,end,by=1),tcl=-0.3,labels=F,lwd=1.3,outer=F)
axis(side=4,at=seq(0,max_depth,by=5),tcl=-0.7,font=1.3,lwd=1.3,outer=F)
axis(side=4,at=seq(0,max_depth,by=1),tcl=-0.3,labels=F,lwd=1.3,outer=F)

#rect(start,0,end,max_depth, col="green", border = NA, density = 24)
#print(no_cover$V2)
#print(no_cover$V3)
#rect(start,0,end,50, col = "white")
#test=as.numeric(start)+100

rect(utr_start,0,utr_end,max_depth, col = "grey",border = NA, density = 48)
rect(no_cover$start,0,no_cover$end,max_depth, col="darkred",border = NA,density= 24)


abline(h=coverage_threshold, col="blue",lwd=1.3)

#threshold_text = "coverage depth threshold"
#mtext(threshold_text,side=2,
#font=0.76,cex=0.8,col="blue",at=coverage_threshold, line=2)

abline(v=no_cover$end, col="red", lwd = 1.3)
mtext(no_cover$end,side=1,font = 0.76,
col="darkred",at=no_cover$end,cex=0.6, line=1)

abline(v=no_cover$start, col="red", lwd = 1.3)
mtext(no_cover$start,side=1,font = 0.76,
col="darkred",at=no_cover$start,cex=0.6, line=0)

title(title_plot,font = 2.6)

par(bg = "white", fg = "black", oma =c(0,0,0,0), mar = c(0,0,0,0), new=TRUE)
plot(0, 0, type = "n", bty = "n", xaxt = "n", yaxt = "n")
legend("bottomleft", legend=c("depth threshold","no cover
region","UTRregion"),bty="n",xpd=TRUE,horiz=TRUE,fill=c("blue","darkred","grey"),border=c("blue","red","grey"),density=c(100,24,48))

invisible(dev.off())
