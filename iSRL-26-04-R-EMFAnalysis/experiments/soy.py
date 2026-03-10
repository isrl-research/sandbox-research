"""
variant,source,e_explicit,m_explicit,f_explicit,e_could_be,m_could_be,f_could_be,e_score,m_score,f_score,zone,uncertain,question_tags
oil,palm | soybean | sunflower | groundnut,NULL,oil,lipid base,cold pressing|refining|solvent extraction,NULL,NULL,0,0.7,0.22,1,True,False
soy,soybean,NULL,NULL,base ingredient,NULL,NULL,NULL,0,0,0.12,1,False,False
tvp,soybean,NULL,protein concentrate,base ingredient,?extrusion,NULL,NULL,0,0.74,0.12,1,True,True
hvp,soybean,?hydrolysis,protein concentrate,base ingredient,NULL,NULL,flavouring agent,0.6,0.74,0.12,2,False,True
tvp,soybean,NULL,protein concentrate,base ingredient,?extrusion,NULL,NULL,0,0.74,0.12,1,True,True
oils,palm | soybean | sunflower | groundnut,NULL,oil,lipid base,cold pressing|refining|solvent extraction,NULL,NULL,0,0.7,0.22,1,True,False
soya,soybean,NULL,NULL,base ingredient,NULL,NULL,NULL,0,0,0.12,1,False,False
soynut,soybean,roasting,NULL,base ingredient,NULL,NULL,NULL,0.58,0,0.12,1,False,False
soynuts,soybean,roasting,whole/fresh pieces,base ingredient,NULL,NULL,NULL,0.58,0.05,0.12,1,False,False
soybean,soybean,NULL,whole/fresh pieces,base ingredient,NULL,NULL,NULL,0,0.05,0.12,1,False,False
soy nuts,soybean,roasting,NULL,base ingredient,NULL,NULL,NULL,0.58,0,0.12,1,False,False
soyabean,soybean,NULL,NULL,base ingredient,NULL,NULL,NULL,0,0,0.12,1,False,False
soybeans,soybean,NULL,NULL,base ingredient,NULL,NULL,NULL,0,0,0.12,1,False,False
cake gel,palm | soybean | sunflower,NULL,NULL,emulsifier|stabiliser,NULL,gelling agent,gelling agent,0,0,0.825,2,False,False
glycerin,palm | soybean | rapeseed,NULL,NULL,humectant,?glycerolysis,NULL,NULL,0,0,0.425,1,False,True
lecithin,soybean | sunflower,solvent extraction,emulsifier powder,emulsifier,NULL,NULL,NULL,0.82,0.89,0.825,3,False,False
vanaspati,palm | soybean | groundnut,hydrogenation|interesterification,fat fraction,lipid base,refining,NULL,NULL,0.92,0.72,0.22,2,False,False
soya grit,soybean,milling,coarse grits,base ingredient,NULL,NULL,NULL,0.28,0.3,0.12,1,False,False
soyabeans,soybean,NULL,whole/fresh pieces,base ingredient,NULL,NULL,NULL,0,0.05,0.12,1,False,False
soya four,soybean,milling,flour/fine powder,base ingredient,NULL,NULL,NULL,0.28,0.33,0.12,1,False,False
glycerine,palm | soybean | rapeseed,?hydrolysis,NULL,humectant,NULL,NULL,NULL,0.6,0,0.425,2,False,True
margarine,palm | soybean | sunflower,interesterification|hydrogenation,fat fraction,lipid base,NULL,NULL,emulsifier,0.92,0.72,0.22,2,True,False
edible oil,palm | soybean | sunflower | groundnut,NULL,oil,lipid base,cold pressing|refining|solvent extraction,NULL,NULL,0,0.7,0.22,1,True,False
soy flakes,soybean,NULL,flakes,base ingredient,NULL,NULL,NULL,0,0.36,0.12,1,False,False
soya seeds,soybean,NULL,whole/fresh pieces,base ingredient,NULL,NULL,NULL,0,0.05,0.12,1,False,False
soya flour,soybean,milling,flour/fine powder,base ingredient,NULL,NULL,NULL,0.28,0.33,0.12,1,False,False
emulsifier,palm | soybean | sunflower,NULL,emulsifier powder,emulsifier,solvent extraction|refining,NULL,stabiliser,0,0.89,0.825,2,True,False
emulsfying,palm | soybean | sunflower,NULL,NULL,emulsifier,solvent extraction|refining,emulsifier powder,stabiliser,0,0,0.825,2,True,False
emuslifier,palm | soybean | sunflower,NULL,emulsifier powder,emulsifier,solvent extraction|refining,NULL,stabiliser,0,0.89,0.825,2,True,False
soya sauce,soybean,fermentation,NULL,flavouring agent,NULL,extract/oleoresin,base ingredient,0.56,0,0.675,2,False,False
cloudifier,palm | soybean | sunflower,NULL,emulsifier powder,emulsifier,NULL,NULL,NULL,0,0.89,0.825,2,False,False
mayonnaise,soybean | sunflower | egg,NULL,emulsifier powder,emulsifier,NULL,NULL,NULL,0,0.89,0.825,2,False,False
refined oil,palm | soybean | sunflower | groundnut,refining,oil,lipid base,cold pressing|solvent extraction,NULL,NULL,0.75,0.7,0.22,2,False,False
soya flakes,soybean,NULL,flakes,base ingredient,NULL,NULL,NULL,0,0.36,0.12,1,False,False
soybean oil,soybean,NULL,oil,lipid base,cold pressing|solvent extraction|refining,NULL,NULL,0,0.7,0.22,1,True,False
emulsifiers,palm | soybean | sunflower,NULL,emulsifier powder,emulsifier,NULL,NULL,NULL,0,0.89,0.825,2,False,False
defatted soy,soybean,NULL,skim/defatted meal,base ingredient,NULL,NULL,NULL,0,0.55,0.12,1,False,False
soyabean oil,soybean,cold pressing|solvent extraction,oil,lipid base,refining,NULL,NULL,0.82,0.7,0.22,2,False,False
soya protein,soybean,NULL,protein concentrate,base ingredient,NULL,protein isolate,NULL,0,0.74,0.12,1,False,False
soy lecithin,soybean | sunflower,solvent extraction,emulsifier,emulsifier,NULL,NULL,NULL,0.82,0.89,0.825,3,False,False
stearic acid,palm | soybean,NULL,crystalline chemical,emulsifier,NULL,NULL,NULL,0,0.98,0.825,2,False,False
vegetable fat,palm | soybean | groundnut,NULL,fat fraction,lipid base,cold pressing|refining|solvent extraction|hydrogenation|interesterification,NULL,NULL,0,0.72,0.22,2,False,False
vegetable oil,palm | soybean | sunflower | groundnut,NULL,oil,lipid base,cold pressing|refining|solvent extraction,NULL,NULL,0,0.7,0.22,1,True,False
soya granules,soybean,NULL,granules,base ingredient,?extrusion,NULL,NULL,0,0.8,0.12,1,True,True
defatted soya,soybean,skim/defatted meal,skim/defatted meal,base ingredient,NULL,NULL,NULL,0,0.55,0.12,1,False,False
soya bean oil,soybean,NULL,oil,lipid base,cold pressing|solvent extraction|refining,NULL,NULL,0,0.7,0.22,1,True,False
soya lecithin,soybean | sunflower,solvent extraction,emulsifier powder,emulsifier,NULL,NULL,NULL,0.82,0.89,0.825,3,False,False
vegetable fats,palm | soybean | groundnut,NULL,fat fraction,lipid base,cold pressing|refining|solvent extraction|hydrogenation|interesterification,NULL,NULL,0,0.72,0.22,2,False,False
vegetable oils,palm | soybean | sunflower | groundnut,NULL,oil,lipid base,cold pressing|refining|solvent extraction,NULL,NULL,0,0.7,0.22,1,True,False
datem ins 472e,palm | soybean | sunflower,interesterification,emulsifier powder,emulsifier,NULL,NULL,NULL,0.91,0.89,0.825,3,False,False
refined soya oil,soybean,refining,oil,lipid base,cold pressing|solvent extraction,NULL,NULL,0.75,0.7,0.22,2,False,False
soy sauce powder,soybean | wheat,fermentation,powder,taste profile / spice,NULL,NULL,flavouring agent,0.56,0.42,0.18,2,False,False
improver ins 472,palm | soybean | sunflower,interesterification,emulsifier powder,emulsifier,NULL,NULL,flour treatment agent,0.91,0.89,0.825,3,False,False
bakery shortening,palm | soybean | groundnut,interesterification,fat fraction,lipid base,hydrogenation,NULL,NULL,0.91,0.72,0.22,2,False,False
hydrogenated oils,palm | soybean | groundnut,hydrogenation,oil,lipid base,NULL,fat fraction,NULL,0.92,0.7,0.22,2,False,False
soya bean extract,soybean,solvent extraction,extract/oleoresin,base ingredient,NULL,NULL,NULL,0.82,0.86,0.12,2,False,False
cake gel ins 470a,palm | soybean | sunflower,NULL,NULL,emulsifier,NULL,emulsifier powder,stabiliser,0,0,0.825,2,False,False
humectant ins 422,palm | soybean | sunflower,NULL,NULL,humectant,NULL,crystalline chemical,sweetener,0,0,0.425,1,True,False
soyabean lecithin,soybean,solvent extraction,emulsifier powder,emulsifier,NULL,NULL,stabiliser,0.82,0.89,0.825,3,False,False
vegetable protein,soybean | groundnut | pea,NULL,protein concentrate,base ingredient,NULL,protein isolate,NULL,0,0.74,0.12,1,False,False
trans fatty acids,palm | soybean | groundnut,hydrogenation|interesterification,fat fraction,lipid base,NULL,oil,NULL,0.92,0.72,0.22,2,False,False
emulsifier ins 442,rapeseed | soybean,NULL,emulsifier powder,emulsifier,NULL,NULL,NULL,0,0.89,0.825,2,False,False
emulsifier ins 429,soybean | sunflower,NULL,emulsifier powder,emulsifier,NULL,NULL,stabiliser,0,0.89,0.825,2,False,False
emulsifier ins 478,palm | soybean | sunflower,NULL,emulsifier powder,emulsifier,NULL,NULL,stabiliser,0,0.89,0.825,2,False,False
emulsifier ins 479,palm | soybean | sunflower,NULL,emulsifier powder,emulsifier,NULL,NULL,stabiliser,0,0.89,0.825,2,False,False
emulsifier ins 475,palm | soybean | sunflower,NULL,emulsifier powder,emulsifier,NULL,NULL,stabiliser,0,0.89,0.825,2,False,False
stabilizer ins 475,palm | soybean | sunflower,NULL,emulsifier powder,stabiliser,NULL,NULL,emulsifier,0,0.89,0.65,2,False,False
emulsifier ins 477,palm | soybean | sunflower,NULL,emulsifier powder,emulsifier,NULL,NULL,stabiliser,0,0.89,0.825,2,False,False
stabilizer ins 477,palm | soybean | sunflower,NULL,emulsifier powder,stabiliser,NULL,NULL,emulsifier,0,0.89,0.65,2,False,False
humectant glycerol,palm | soybean | sunflower,NULL,NULL,humectant,NULL,NULL,NULL,0,0,0.425,1,False,False
emulsifier ins 322,soybean | sunflower,NULL,emulsifier powder,emulsifier,NULL,NULL,stabiliser,0,0.89,0.825,2,False,False
stabilizer ins 322,soybean | sunflower,NULL,emulsifier powder,stabiliser,NULL,NULL,emulsifier,0,0.89,0.65,2,False,False
emulsifier ins 471,palm | soybean | sunflower,NULL,emulsifier powder,emulsifier,NULL,NULL,stabiliser,0,0.89,0.825,2,False,False
stabilizer ins 471,palm | soybean | sunflower,NULL,emulsifier powder,stabiliser,NULL,NULL,emulsifier,0,0.89,0.65,2,False,False
stabilizer ins 472,palm | soybean | sunflower,interesterification,emulsifier powder,emulsifier|stabiliser,NULL,NULL,NULL,0.91,0.89,0.825,3,False,False
defatted soya flour,soybean,skim/defatted meal|milling,flour/fine powder,base ingredient,NULL,NULL,NULL,0.28,0.33,0.12,1,False,False
soya flour defatted,soybean,skim/defatted meal|milling,flour/fine powder,base ingredient,NULL,NULL,NULL,0.28,0.33,0.12,1,False,False
soy protein isolate,soybean,NULL,protein isolate,base ingredient,NULL,NULL,NULL,0,0.78,0.12,1,False,False
emulsifier ins 4806,palm | soybean | sunflower,NULL,NULL,emulsifier,NULL,NULL,stabiliser,0,0,0.825,2,False,False
stabilizer ins 4806,palm | soybean | sunflower,NULL,NULL,stabiliser,NULL,NULL,thickener|gelling agent,0,0,0.65,1,False,False
emulsifier tween 80,palm | soybean | sunflower,NULL,emulsifier powder,emulsifier,NULL,NULL,NULL,0,0.89,0.825,2,False,False
emulsifier lecithin,soybean | sunflower,NULL,emulsifier powder,emulsifier,solvent extraction,oil,NULL,0,0.89,0.825,2,True,False
emulsifier ins 4726,palm | soybean | sunflower,NULL,emulsifier powder,emulsifier,NULL,NULL,NULL,0,0.89,0.825,2,False,False
emulsifier ins 472b,palm | soybean | sunflower,NULL,emulsifier powder,emulsifier,NULL,NULL,NULL,0,0.89,0.825,2,False,False
emulsifier ins 472c,palm | soybean | sunflower,NULL,emulsifier powder,emulsifier,NULL,NULL,NULL,0,0.89,0.825,2,False,False
vegetable shortening,palm | soybean | groundnut,hydrogenation|interesterification,fat fraction,lipid base,refining,NULL,NULL,0.92,0.72,0.22,2,False,False
edible vegetable fat,palm | soybean | sunflower | groundnut,refining,fat fraction,lipid base,cold pressing|solvent extraction,NULL,NULL,0.75,0.72,0.22,2,False,False
edible vegetable oil,palm | soybean | sunflower | groundnut,refining,oil,lipid base,cold pressing|solvent extraction,NULL,NULL,0.75,0.7,0.22,2,False,False
edible vegeteble oil,palm | soybean | sunflower | groundnut,refining,oil,lipid base,cold pressing|solvent extraction,NULL,NULL,0.75,0.7,0.22,2,False,False
refined soyabean oil,soybean,refining,oil,lipid base,cold pressing|solvent extraction,NULL,NULL,0.75,0.7,0.22,2,False,False
soya protein isolate,soybean,NULL,protein isolate,base ingredient,solvent extraction,NULL,NULL,0,0.78,0.12,1,True,False
sorbitan tristearate,palm | soybean | sunflower,interesterification,emulsifier powder,emulsifier,NULL,NULL,NULL,0.91,0.89,0.825,3,False,False
emulsifier lecithins,soybean | sunflower,solvent extraction,extract/oleoresin,emulsifier,NULL,NULL,NULL,0.82,0.86,0.825,3,False,False
emulsifier ins 472 e,palm | soybean | sunflower,interesterification,emulsifier powder,emulsifier,NULL,NULL,NULL,0.91,0.89,0.825,3,False,False
edible vegetable fats,palm | soybean | groundnut | sunflower,NULL,fat fraction,lipid base,cold pressing|refining|solvent extraction|hydrogenation|interesterification,oil,NULL,0,0.72,0.22,2,False,False
refined vegetable oil,palm | soybean | sunflower | groundnut,refining,oil,lipid base,cold pressing|solvent extraction,NULL,NULL,0.75,0.7,0.22,2,False,False
sorbitean tristearate,palm | soybean | sunflower,interesterification,NULL,emulsifier,NULL,crystalline chemical,NULL,0.91,0,0.825,2,True,False
emulsifiers lecithins,soybean | sunflower,solvent extraction,extract/oleoresin,emulsifier,NULL,NULL,NULL,0.82,0.86,0.825,3,False,False
soya lecithin ins 322,soybean,solvent extraction,extract/oleoresin,emulsifier,NULL,NULL,NULL,0.82,0.86,0.825,3,False,False
mono and diglycerides,palm | soybean | sunflower,interesterification,NULL,emulsifier,NULL,NULL,NULL,0.91,0,0.825,2,False,False
mono-and diglycerides,palm | soybean | sunflower,interesterification,NULL,emulsifier,NULL,NULL,NULL,0.91,0,0.825,2,False,False
soya sauce flavouring,soybean | wheat,fermentation,extract/oleoresin,flavouring agent,NULL,NULL,taste profile / spice,0.56,0.86,0.675,2,False,False
hydrogenated table oil,palm | soybean | groundnut,hydrogenation,oil,lipid base,cold pressing|refining|solvent extraction,NULL,NULL,0.92,0.7,0.22,2,False,False
emulsifier soy ins 322,soybean,solvent extraction,emulsifier powder,emulsifier,NULL,extract/oleoresin,NULL,0.82,0.89,0.825,3,False,False
emulsifier soy lecithin,soybean,solvent extraction,emulsifier powder,emulsifier,NULL,extract/oleoresin,NULL,0.82,0.89,0.825,3,False,False
anticaking agent ins 470,palm | soybean | sunflower,NULL,crystalline chemical,anticaking agent,NULL,emulsifier powder,emulsifier,0,0.98,0.85,2,False,False
soya protein hydrolysate,soybean,?hydrolysis,protein concentrate,base ingredient,NULL,protein isolate,NULL,0.6,0.74,0.12,2,False,True
emulsifier soya lecithin,soybean,solvent extraction,extract/oleoresin,emulsifier,NULL,NULL,NULL,0.82,0.86,0.825,3,False,False
emulsifier soya lecothin,soybean,solvent extraction,extract/oleoresin,emulsifier,NULL,NULL,NULL,0.82,0.86,0.825,3,False,False
emulsifier soya lecithins,soybean,solvent extraction,extract/oleoresin,emulsifier,NULL,NULL,NULL,0.82,0.86,0.825,3,False,False
emulsifier – lecithin soy,soybean,solvent extraction,extract/oleoresin,emulsifier,NULL,NULL,NULL,0.82,0.86,0.825,3,False,False
stabilising agent ins 471,palm | soybean | sunflower,NULL,NULL,stabiliser|emulsifier,NULL,NULL,NULL,0,0,0.825,2,False,False
stabilizing agent ins 471,palm | soybean | sunflower,NULL,NULL,stabiliser|emulsifier,NULL,NULL,NULL,0,0,0.825,2,False,False
hydrogenated vegetable fat,palm | soybean | groundnut,hydrogenation,fat fraction,lipid base,NULL,NULL,NULL,0.92,0.72,0.22,2,False,False
hydrogenated vegetable oil,palm | soybean | groundnut,hydrogenation,oil,lipid base,NULL,NULL,NULL,0.92,0.7,0.22,2,False,False
fractionated vegetable fat,palm | soybean | groundnut,fractionation,fat fraction,lipid base,NULL,NULL,NULL,0.76,0.72,0.22,2,False,False
partially hydrogenated oil,palm | soybean | groundnut,hydrogenation,oil,lipid base,NULL,NULL,NULL,0.92,0.7,0.22,2,False,False
magnesium stearate ins 470,palm | soybean | sunflower,NULL,crystalline chemical,anticaking agent|emulsifier,NULL,NULL,NULL,0,0.98,0.85,2,False,False
hydrogenated vegetable fats,palm | soybean | groundnut,hydrogenation,fat fraction,lipid base,cold pressing|refining|solvent extraction,oil,NULL,0.92,0.72,0.22,2,False,False
fractionated vegetable fats,palm | soybean | groundnut,fractionation,fat fraction,lipid base,cold pressing|refining|solvent extraction,oil,NULL,0.76,0.72,0.22,2,False,False
emulsifier vegetable origin,palm | soybean | sunflower,NULL,emulsifier powder,emulsifier,NULL,NULL,NULL,0,0.89,0.825,2,False,False
hydrolyzed vegetable protein,soybean | groundnut | corn,?hydrolysis,protein concentrate,base ingredient,NULL,NULL,flavouring agent,0.6,0.74,0.12,2,False,True
hydrolysed vegetable protein,soybean | groundnut | corn,?hydrolysis,protein concentrate,base ingredient,NULL,NULL,flavouring agent,0.6,0.74,0.12,2,False,True
hydralyzed vegetable protein,soybean | groundnut | corn,?hydrolysis,protein concentrate,base ingredient,NULL,NULL,flavouring agent,0.6,0.74,0.12,2,False,True
hydrolized vegetable protein,soybean | groundnut | corn,?hydrolysis,protein concentrate,base ingredient,NULL,NULL,flavouring agent,0.6,0.74,0.12,2,False,True
interesterified vegetable fat,palm | soybean | groundnut,interesterification,fat fraction,lipid base,cold pressing|refining|solvent extraction|hydrogenation,oil,NULL,0.91,0.72,0.22,2,False,False
texturised soy protein flakes,soybean,?extrusion,protein concentrate|flakes,base ingredient,NULL,NULL,NULL,0.6,0.74,0.12,2,False,True
edible vanaspati oil vanaspati,palm | soybean | groundnut,hydrogenation|interesterification,oil,lipid base,cold pressing|refining|solvent extraction,NULL,NULL,0.92,0.7,0.22,2,False,False
soya sauce powder lodized salt,soybean | mineral,fermentation,powder,taste profile / spice,NULL,NULL,flavouring agent,0.56,0.42,0.18,2,False,False
emulsifier soy lecithin ins 322,soybean,NULL,emulsifier powder,emulsifier,solvent extraction,extract/oleoresin,antioxidant,0,0.89,0.825,2,True,False
emulsifying agent soya lecithin,soybean,NULL,emulsifier powder,emulsifier,solvent extraction,extract/oleoresin,antioxidant,0,0.89,0.825,2,True,False
emulsifier ins 471 plant origin,palm | soybean | sunflower,NULL,emulsifier powder,emulsifier,interesterification|solvent extraction,extract/oleoresin,stabiliser,0,0.89,0.825,2,True,False
emulsifier soya lecithin ins 322,soybean | sunflower,solvent extraction,emulsifier powder,emulsifier,NULL,extract/oleoresin,NULL,0.82,0.89,0.825,3,False,False
emulsifier glyceryl monostearate,palm | soybean | sunflower,interesterification,emulsifier powder,emulsifier,NULL,NULL,NULL,0.91,0.89,0.825,3,False,False
emulsifier salts of stearic acid,palm | soybean | sunflower,NULL,crystalline chemical,emulsifier,NULL,NULL,NULL,0,0.98,0.825,2,False,False
hydrogenated edible vegetable fat,palm | soybean | groundnut,hydrogenation,fat fraction,lipid base,cold pressing|refining|solvent extraction,NULL,NULL,0.92,0.72,0.22,2,False,False
hydrogenated vegetable oil vanaspati,palm | soybean | groundnut,hydrogenation|refining,oil,lipid base,cold pressing|solvent extraction,fat fraction,NULL,0.92,0.7,0.22,2,False,False
edible vegetable fat onteresterified,palm | soybean | sunflower | groundnut,interesterification|refining,fat fraction,lipid base,cold pressing|solvent extraction,oil,NULL,0.91,0.72,0.22,2,False,False
emulsifier sodium stearoyl lactylate,palm | soybean | sunflower,NULL,emulsifier powder,emulsifier,NULL,NULL,NULL,0,0.89,0.825,2,False,False
mono- and diglycerides of fatty acids,palm | soybean | sunflower,interesterification,emulsifier powder,emulsifier,NULL,NULL,NULL,0.91,0.89,0.825,3,False,False
edible vegetable fat bakery shortening,palm | soybean | groundnut,NULL,fat fraction,lipid base,hydrogenation|interesterification|refining,oil,NULL,0,0.72,0.22,2,False,False
stabilizer hydrolysed vegetable protein,soybean | groundnut,?hydrolysis,protein concentrate,stabiliser,NULL,NULL,base ingredient|flavouring agent,0.6,0.74,0.65,2,False,True
stabilizer hydrolyzed vegetable protein,soybean | groundnut,?hydrolysis,protein concentrate,stabiliser,NULL,NULL,base ingredient|flavouring agent,0.6,0.74,0.65,2,False,True
emulsifier di-glycerides of fatty acids,palm | soybean | sunflower,NULL,lipid base,emulsifier,interesterification,NULL,NULL,0,0,0.825,2,False,False
interesterified vegetable fat sesame oil,palm | soybean | groundnut | sesame,interesterification,fat fraction|oil,lipid base,refining|solvent extraction|cold pressing,NULL,NULL,0.91,0.72,0.22,2,False,False
emulsifier polyglycerol esters of fatty acid,palm | soybean | sunflower,interesterification,emulsifier powder,emulsifier,NULL,NULL,NULL,0.91,0.89,0.825,3,False,False
partially hydrogenated refined vegetable oils,palm | soybean | groundnut,refining|hydrogenation,oil,lipid base,cold pressing|solvent extraction,NULL,NULL,0.92,0.7,0.22,2,False,False
stabilizer mono and diglycerides of fatty acids,palm | soybean | sunflower,interesterification,fat fraction,stabiliser|emulsifier,NULL,NULL,NULL,0.91,0.72,0.825,3,False,False
emulsifier mono- and diglycerides of fatty acids,palm | soybean | sunflower,interesterification,fat fraction,emulsifier|stabiliser,NULL,NULL,NULL,0.91,0.72,0.825,3,False,False
emulsifier propylene glycol esters of fatty acids,palm | soybean | sunflower,acetylation,fat fraction,emulsifier,NULL,NULL,stabiliser,0.94,0.72,0.825,3,False,False
emulsifiers mono- and diglycerides of fatty acids,palm | soybean | sunflower,interesterification,fat fraction,emulsifier|stabiliser,NULL,NULL,NULL,0.91,0.72,0.825,3,False,False
emulsifier mono and diglycerides of fatty acids ins 471,palm | soybean | sunflower,interesterification,fat fraction,emulsifier|stabiliser,NULL,NULL,NULL,0.91,0.72,0.825,3,False,False
emulsifier diacetyl tartaric acid ester of mono and diglycerides,palm | soybean | sunflower,interesterification,emulsifier powder,emulsifier,NULL,NULL,NULL,0.91,0.89,0.825,3,False,False
di-acetyl tartaric acid esters of mono and diglycerides of edible vegetable oils,palm | soybean | sunflower | groundnut,interesterification,oil,emulsifier,NULL,emulsifier powder,NULL,0.91,0.7,0.825,3,False,False
emulsifier di-acetyl tartaric acid esters of mono and diglycerides of edible vegetable oils,palm | soybean | sunflower | groundnut,interesterification,emulsifier powder,emulsifier,NULL,oil,NULL,0.91,0.89,0.825,3,False,False
emulsifier di-acetyl tartaric acid esters of mono and di-glycerides of edible vegetable oils,palm | soybean | sunflower | groundnut,interesterification,emulsifier powder,emulsifier,NULL,oil,NULL,0.91,0.89,0.825,3,False,False

"""