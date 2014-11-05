
figure(1)
scatter(language(:,1),language(:,2))

figure(2)
imagesc(vgrid)



figure(4)
l = sortrows(language,-2);
plot(l(:,2))
set(gca,'XScale','log')
set(gca,'YScale','log')

figure(5)
plot(growth)

figure(3)
h = scatter(vocab(:,1),vocab(:,2));
set(h,'CData',vocab(:,2))

 
 set(gca,'CLim',[min(vocab(:,2)), max(vocab(:,2))])


