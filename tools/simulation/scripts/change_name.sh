 #!/bin/bash
 regex="(C_[[:digit:]].E_[[:digit:]]_)"
 for i in $( ls ); do

  #echo $i | grep -Ei 'C\_[0-9]+\.E\_[0-9]+\_' | grep -oEi 'C\_[0-9]+\.E\_[0-9]+\_'
f=$(echo $i | grep -Ei 'C\_[0-9]+\.E\_[0-9]+\_' | grep -oEi 'C\_[0-9]+\.E\_[0-9]+\_')

   #echo $f


   mv -i "$i" "${f}5"


 done
