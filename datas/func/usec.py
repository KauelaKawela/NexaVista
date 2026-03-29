import clr,sys

def uzanti_sec():
      try:
            uzantilar = {1:"txt",2:"json",3:"csv",4:"xml",5:"html"}
            print(f"\n{clr.k} 1- [{clr.r}txt{clr.k}]\t2- [{clr.r}json{clr.k}]\t3- [{clr.r}csv{clr.k}]\t4- [{clr.r}xml{clr.k}]\n\n 5- [{clr.r}html{clr.k}]\t6- [{clr.r}???{clr.k}]\t7- [{clr.r}???{clr.k}]\t8- [{clr.r}???{clr.k}]\n")
            usecim = int(input(f"{clr.am4}╠ > Dosya uzantisi seciniz: {clr.r}"))
            if usecim in uzantilar:
                return uzantilar[usecim]
            else:
                raise ValueError()
      except ValueError:
            print(f"{clr.am9}║\n║\n{clr.am5}╚════════════╝ {clr.k}Hatali secim! Gecerli uzanti giriniz {clr.r}")
            sys.exit()