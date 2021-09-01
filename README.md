# Simulacijsko-okolje-za-generiranje-vodnih-scen

## 1. Zahteve:

Ves projekt je bil narejen z naslednjimi zahtevami:

- Python verzija: >= 3.9.4  https://www.python.org/downloads/ (pip je že vključen, potrebno ga je dodati v path)
- pip verzija: 21.1
- Blender verzija 2.91 https://www.blender.org/download/releases/2-91/
- Testirano na windows operacijskem sistemu.

## 2. Uporaba:

Za uporabo simulacijskega okolja je poleg kloniranja repozitorija, potrebno narediti naslednje stvari:

### a) Blender pot

V config.yaml datoteki, ki se nahaja pod *ocean/OceanA* ali *ocean/OceanB* je potrebno dodati pot do programa Blender.

![image](https://user-images.githubusercontent.com/47794629/131579565-396031da-42cd-4df1-a6a2-f80b3c5a4656.png)
    
###  b) Izrezane ovire
Primeri slik iz COCO zbirke so pod *images/*, če pa želite dostopati do celotne zbirke pa je potrebno naložiti 
- COCO train http://images.cocodataset.org/zips/train2017.zip (18GB) ali
- COCO val http://images.cocodataset.org/zips/val2017.zip (1GB)
- anotacije hribov in gora http://calvin.inf.ed.ac.uk/wp-content/uploads/data/cocostuffdataset/stuff_trainval2017.zip
- anotacije čolnov in boj https://s3-us-west-2.amazonaws.com/dl.fbaipublicfiles.com/LVIS/lvis_v1_train.json.zip in https://s3-us-west-2.amazonaws.com/dl.fbaipublicfiles.com/LVIS/lvis_v1_val.json.zip

Pridobljene slike je potrebno unzipati in prestaviti v mapi *resources/COCO_train* in *resources/COCO_val*. Naložene anotacije je ravno tako potrebno unzipati vendar v mapo       *resources/annotations*. Izrezane slike se pridobi s skripto get_segmented_pics.py v mapi */scripts*. Z argumentoma lahko povemo kateri objekt želimo in pa katere anotacije         bomo uporabili. Nastala mapa bo enaka kot **object_type** v */resources/**object_type***.
    
Primer ukaza:
    
 ```
 python get_segmented_pics.py --object_type boat --annotation_type lvis_v1_train
 ```
### c) Haven nebo
V mapi *resources/Haven/hdris* je primer Haven .hdr datoteke neba. Če želimo pridobiti več Haven datotek uporabimo skripto **download_haven.py** v mapi */scripts*

Primer uporabe:
  
```
python download_haven.py --types hdris --categories skies --resolution 4k
```
### d) Postopek generiranja
Generiranje oceana lahko poženemo na dva načina:
    
i) S skripto *run.py*
   
```
python run.py ocean/OceanA/config.yaml ocean/OceanA/camera_position ocean/OceanA/OceanA.blend outputs/Output0 resources\Haven\ resources/boats resources/mountains resources/buoys
```
ali
  
ii) S skripto *run_multiple_times.py*
    
   #### Argumenti
* `config_file` - <i>pot do config.yaml datoteke</i>
* `cam_file` - <i>pot do konfiguracije kamere</i>
* `blend_file` - <i>pot do .blend datoteke</i>
* `output_path` - <i>pot do mape, kamor se bodo generirale slike</i>
* `haven_dir` - <i>pot do mape s Haven .hdr datotekami</i>
* `boat_dir` - <i>pot do mape z izrezanimi čolni</i>
* `mountain_dir` - <i>pot do mape z izrezanimi gorami</i>
* `buoy_dir` - <i>pot do mape z izrezanimi bojami</i>
* `starting_output` - <i>število s katero naj se začne generiranje podatkov</i> 
* `number_of_outputs` - <i>število koliko slik naj se generira</i>

 Primer uporabe skripte s privzetimi nastavitvami:
    
 ```
 python run_multiple_times.py 
 ```
### e) Razne skripte
Ko imamo generirano zbirko s skripto **move_outputs_to_images.py** premaknemo vse outpute v isti folder in sicer v *images/*. Ko imamo slike v *images/* lahko naredimo prenos barv s skripto **transferColors.m**, spremenimo segmentacijske slike, da so pripravljene za treniranje mreže WaSR s skripto **seg_to_my_seg.py**. Za treniranje potrebujemo tudi train.txt datoteko z vsebino zbirke, ki jo lahko naredimo z skripto **create_train_text.py**.

## 3. Primeri generiranih slik:

Generirane slike             |  Segmentacijske slike
:-------------------------:|:-------------------------:
![rgb_0001](https://user-images.githubusercontent.com/47794629/131576220-91c55022-225f-4df7-a572-0cddbd6fd57b.png)  |  ![segmap_0001](https://user-images.githubusercontent.com/47794629/131576224-991eab5f-c237-48d0-9406-bcda5d77113b.png)
![rgb_0002](https://user-images.githubusercontent.com/47794629/131576487-fcb25e3f-8a79-4666-bef0-dc1f54bbae16.png) | ![segmap_0002](https://user-images.githubusercontent.com/47794629/131576536-e7ef7cc4-1250-435e-aebe-8170a3b6d80a.png)
![rgb_0001](https://user-images.githubusercontent.com/47794629/131577367-02845029-c3ef-43ed-ab03-c1488838013c.png) | ![segmap_0001](https://user-images.githubusercontent.com/47794629/131577372-a2a2cff9-c32b-4c71-bb7c-3195ebad6dd7.png)

# 4. Reference

[1] Bovcon et. al, The MaSTr1325 Dataset for Training Deep USV Obstacle Detection Models, IROS 2019 <br>
[2] COCO zbirka in anotacije https://github.com/nightrome/cocostuff <br>
[3] LVIS anotacije https://www.lvisdataset.org/dataset <br>
[4] BlenderProc https://github.com/DLR-RM/BlenderProc <br>
[5] Haven HDRIs https://polyhaven.com/hdris
[6] Color transfer between images https://www.mathworks.com/matlabcentral/fileexchange/63256-color-transfer-between-images
[7] Navdih za ocean A: https://www.youtube.com/watch?v=CwJrb3vjAaA&t=216s
[8] Navdih za ocean B: https://www.youtube.com/watch?v=nOdNUFPbBJM
