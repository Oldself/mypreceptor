from django.utils import simplejson as json
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db

class TestVO(db.Model):
    id = db.StringProperty()
    title = db.StringProperty(default='no title')
    author = db.UserProperty()
    content = db.BlobProperty()
    
def getTestVO(user, testId):
    """Return the stored TestVO or None."""
    if not(user):
        return None
    testVOs = TestVO.gql("WHERE author = :1 AND id = :2 ORDER BY title ASC LIMIT 100", user, testId)
    for testVO in testVOs:      # un peu boeuf, peut mieux faire !
        return testVO

class MyHandler(webapp.RequestHandler):
    def get(self):
        #----------------------------------------------------
        # functions for any user, even not authenticated
        #----------------------------------------------------
        
        
        
        #----------------------------------------------------
        # from here an identified user is required
        #----------------------------------------------------

        user = users.get_current_user()
        if not(user):
            #self.response.out.write("<html><body>Authentifiez vous d'abord</body></html>");
            result = ["AUTHENTICATE", users.create_login_url("/app/index.html")]
            self.response.out.write(json.dumps(result))
            return
        
        action = self.request.get('action')
        testId = self.request.get('testId')
        #
        # GET LIST
        #
        if action == "getUserTests":
            testVOs = TestVO.gql("WHERE author = :1 ORDER BY title ASC LIMIT 100", user)
            result = [];
            for testVO in testVOs:
                result.append([testVO.id, testVO.title])
            self.response.out.write(json.dumps(result));
            return
        
        #
        # SAVE
        #
        if action == "saveTest":
            testVO = getTestVO(user, testId)
            if not(testVO):
                testVO = TestVO()
                testVO.id = testId
                testVO.author = user
            testVO.content = self.request.get('testDTO').encode('utf-8')
            testVO.title = self.request.get('title')
            testVO.save()   # create or update
            self.response.out.write(json.dumps(testId))
            return
        
        #
        # GET
        #
        if (action == "getTest"):
            testVO = getTestVO(user, testId)
            if testVO:
                self.response.out.write(testVO.content);
            return
        
        #
        # DELETE
        #
        if action == "deleteTest":
            testVO = getTestVO(user, testId)
            if testVO:
                testVO.delete();
                self.response.out.write(json.dumps("ok"))
            return
        
        #
        # INIT
        #
        if action == "init":
            result = [user.nickname(), users.create_logout_url("/app/index.html"), users.create_login_url("/app/index.html"), users.is_current_user_admin()]    
            self.response.out.write(json.dumps(result))
            return
            
        #----------------------------------------------------
        # From here, only admin is allowed
        #----------------------------------------------------

        if not(users.is_current_user_admin()):
            return
            
        if action == "listUsers":
            testVOs = TestVO.all();
            byUser = {};
            for testVO in testVOs:
                if testVO.author.nickname() in byUser:
                    byUser[testVO.author.nickname()] += 1
                else:
                    byUser[testVO.author.nickname()] = 1
            result = []
            for key, value in byUser.iteritems():
                result.append([key, value])
            self.response.out.write(json.dumps(result))
            
#        if action == "aloha":
#            tests = json.loads(aloha)
#            for test in tests:
#                testId = test['id']
#                testVO = getTestVO(user, testId)
#                if not(testVO):
#                    testVO = TestVO()
#                    testVO.id = testId
#                    testVO.author = user
#                testVO.content = str(json.dumps(test))
#                testVO.title = test['title']
#                testVO.save()   # create or update
#            
#        if action == "aglae":
#            tests = json.loads(aglae)
#            for test in tests:
#                testId = test['id']
#                testVO = getTestVO(user, testId)
#                if not(testVO):
#                    testVO = TestVO()
#                    testVO.id = testId
#                    testVO.author = user
#                testVO.content = str(json.dumps(test))
#                testVO.title = test['title']
#                testVO.save()   # create or update
                
            
    def post(self):
        self.get();

application = webapp.WSGIApplication([('/.*', MyHandler)], debug=True)

#aloha="""[{"title":"Latin vocab. 24\/10 F=>L","id":"1350834554033","testItemVOs":[{"question":"\u00eatre","response":"sum es esse fui","type":""},{"question":"pouvoir","response":"possum potes posse potui","type":""},{"question":"honorer","response":"colo is ere colui cultum","type":""},{"question":"voir","response":"video es ere vidi visum","type":""},{"question":"aller","response":"eo is ire ivi itum","type":""},{"question":"sortir","response":"exeo is ire ivi itum","type":""},{"question":"prendre","response":"capio is ere cepi captum","type":""},{"question":"aimer ","response":"amo as are avi atum","type":""},{"question":"donner","response":"do as are dedi datum","type":""},{"question":"appeler","response":"voco as are avi atum","type":""},{"question":"craindre","response":"timeo es ere timui","type":""},{"question":"avoir (poss\u00e9der)","response":"habeo es ere habui habitum","type":""},{"question":"conduire","response":"duco is ere duxi ductum","type":""},{"question":"entendre","response":"audio is ire ivi itum","type":""},{"question":"envoyer","response":"mitto is ere misi missum","type":""}]},{"title":"Anglais - verbes irreguliers","id":"1350834567906","testItemVOs":[{"question":"acheter","response":"buy bought bought","type":""},{"question":"apporter","response":"bring brought brought","type":""},{"question":"couper","response":"cut cut cut","type":""}]},{"title":"Latin, vocabulaire pour le 5\/12\/12","id":"1353513933486","testItemVOs":[{"question":"la mort","response":"mors mortis f","type":""},{"question":"le compagnon, la compagne","response":"comes comitis m f","type":""},{"question":"le destin","response":"fatum i n","type":""},{"question":"la maladie","response":"morbus i m","type":""},{"question":"l'h\u00f4te","response":"hospes hospitis m","type":""},{"question":"vivre","response":"vivo is ere vixi victum","type":""},{"question":"traverser","response":"transeo is ire ivi itum","type":""},{"question":"maintenant","response":"num nunc","type":""},{"question":"toujours","response":"semper","type":""},{"question":"bien","response":"bene","type":""}]},{"title":"","id":"1354638019966","testItemVOs":[{"question":"semper","response":"toujours","type":""},{"question":"mors mortis f","response":"la mort","type":""},{"question":"morbus i m","response":"la maladie","type":""},{"question":"comes comitis m f ","response":"le compagnon la compagne","type":""},{"question":"num nunc","response":"maintenant","type":""},{"question":"bene","response":"bien","type":""},{"question":"fatum i n","response":"le destin","type":""}]},{"title":"Latin, vocabulaire pour le 5\/12\/12 L=>F","id":"1354638107463","testItemVOs":[{"question":"fatum i n","response":"le destin","type":""},{"question":"mors mortis f","response":"la mort","type":""},{"question":"morbus i m","response":"la maladie","type":""},{"question":"comes comitis m f ","response":"le compagnon la compagne","type":""},{"question":"hospes hospitis m","response":"l'h\u00f4te","type":""},{"question":"num nunc","response":"maintenant","type":""},{"question":"semper","response":"toujours","type":""},{"question":"bene","response":"bien","type":""},{"question":"vivo is ere vixi victum","response":"vivre","type":""},{"question":"transeo is ire ivi itum","response":"traverser","type":""}]},{"title":"Anglais-verbes irr\u00e9guliers (B)","id":"1355062666310","testItemVOs":[{"question":"\u00eatre","response":"be was were been","type":""},{"question":"porter supporter (n\u00e9)","response":"bear bore born borne","type":""},{"question":"battre","response":"beat beat beaten","type":""},{"question":"devenir","response":"become became become","type":""},{"question":"commencer","response":"begin began begun","type":""},{"question":"mordre","response":"bite bit bitten","type":""},{"question":"saigner","response":"bleed bled bled","type":""},{"question":"souffler","response":"blow blew blown","type":""},{"question":"casser","response":"break broke broken","type":""},{"question":"apporter","response":"bring brought brought","type":""},{"question":"diffuser \u00e9mettre","response":"broadcast broadcast broadcast","type":""},{"question":"construire","response":"build built built","type":""},{"question":"br\u00fbler","response":"burn burnt burnt ","type":""},{"question":"acheter","response":"buy bought bought","type":""},{"question":"be","response":"be was were been \u00eatre","type":""},{"question":"bear ","response":"bear bore born borne porter supporter","type":""},{"question":"beat","response":"beat beat beaten battre","type":""},{"question":"become","response":"become became become devenir","type":""},{"question":"begin","response":"begin began begun commencer","type":""},{"question":"bite","response":"bite bit bitten modre","type":""},{"question":"bleed","response":"bleed bled bled saigner","type":""},{"question":"blow","response":"blow blew blown souffler","type":""},{"question":"break","response":"break broke broken casser","type":""},{"question":"bring","response":"bring brought brought apporter ","type":""},{"question":"broadcast","response":"broadcast broadcast broadcast diffuser \u00e9mettre","type":""},{"question":"build","response":"build built built construire","type":""},{"question":"burn","response":"burn burnt burnt br\u00fbler","type":""},{"question":"buy","response":"buy bought bought acheter","type":""}]},{"title":"Anglais-verbes irr\u00e9guliers (C\/D)","id":"1355649013797","testItemVOs":[{"question":"catch ","response":"catch caught caught attraper","type":""},{"question":"attraper","response":"catch caught caught","type":""},{"question":"choose ","response":"choose chose chosen choisir","type":""},{"question":"choisir","response":"choose chose chosen","type":""},{"question":"come","response":"come came come venir","type":""},{"question":"venir","response":"come came come","type":""},{"question":"cost","response":"cost cost cost co\u00fbter","type":""},{"question":"co\u00fbter","response":"cost cost cost","type":""},{"question":"cut","response":"cut cut cut couper","type":""},{"question":"couper","response":"cut cut cut","type":""},{"question":"do","response":"do did done faire","type":""},{"question":"faire","response":"do did done","type":""},{"question":"draw ","response":"draw drew drawn dessiner","type":""},{"question":"dessiner","response":"draw drew drawn","type":""},{"question":"dream","response":"dream dreamt dreamt r\u00eaver","type":""},{"question":"r\u00eaver","response":"dream dreamt dreamt","type":""},{"question":"drink","response":"drink drank drunk boire","type":""},{"question":"boire","response":"drink drank drunk","type":""},{"question":"drive ","response":"drive drove driven conduire","type":""},{"question":"conduire","response":"drive drove driven","type":""}]},{"title":"Anglais-verbes irr\u00e9guliers (E\/F)","id":"1355649994962","testItemVOs":[{"question":"eat ","response":"eat ate eaten manger","type":""},{"question":"manger","response":"eat ate eaten","type":""},{"question":"fall ","response":"fall fell fallen tomber","type":""},{"question":"tomber","response":"fall fell fallen","type":""},{"question":"feed ","response":"feed fed fed nourrir","type":""},{"question":"nourrir","response":"feed fed fed ","type":""},{"question":"feel ","response":"feel felt felt sentir ressentir","type":""},{"question":"sentir ressentir","response":"feel felt felt","type":""},{"question":"fight","response":"fight fought fought combattre se battre","type":""},{"question":"combattre se battre","response":"fight fought fought","type":""},{"question":"find","response":"find found found trouver","type":""},{"question":"trouver","response":"find found found","type":""},{"question":"fly ","response":"fly flew flown voler","type":""},{"question":"voler","response":"fly flew flown ","type":""},{"question":"forbid","response":"forbid forbade forbidden interdire","type":""},{"question":"interdire","response":"forbid forbade forbidden","type":""},{"question":"forget","response":"forget forgot forgotten oublier","type":""},{"question":"oublier","response":"forget forgot forgotten","type":""},{"question":"forgive ","response":"forgive forgave forgiven pardonner","type":""},{"question":"pardonner","response":"forgive forgave forgiven","type":""},{"question":"freeze","response":"freeze froze frozen geler","type":""},{"question":"geler","response":"freeze froze frozen","type":""}]},{"title":"Anglais-verbes irr\u00e9guliers (G\/H)","id":"1355853033436","testItemVOs":[{"question":"get","response":"get got got obtenir devenir","type":""},{"question":"obtenir","response":"get got got","type":""},{"question":"give","response":"give gave given donner","type":""},{"question":"donner","response":"give gave given","type":""},{"question":"go","response":"go went gone aller","type":""},{"question":"aller","response":"go went gone","type":""},{"question":"grow","response":"grow grew grown grandir faire pousser","type":""},{"question":"grandir faire pousser","response":"grow grew grown","type":""},{"question":"hang","response":"hang hung hung accrocher","type":""},{"question":"accrocher","response":"hang hung hung","type":""},{"question":"have ","response":"have had had avoir","type":""},{"question":"avoir ","response":"have had had","type":""},{"question":"hear","response":"hear heard heard entendre","type":""},{"question":"entendre","response":"hear heard heard","type":""},{"question":"hide","response":"hide hid hidden se cacher","type":""},{"question":"hit","response":"hit hit hit frapper","type":""},{"question":"hold","response":"hold held held tenir","type":""},{"question":"frapper ","response":"hit hit hit","type":""},{"question":"tenir","response":"hold held held","type":""},{"question":"hurt","response":"hurt hurt hurt faire mal blesser","type":""},{"question":"faire mal blesser","response":"hurt hurt hurt","type":""}]},{"title":"Anglais-verbes irr\u00e9guliers (K\/L)","id":"1357585085699","testItemVOs":[{"question":"keep","response":"keep kept kept garder","type":""},{"question":"garder","response":"keep kept kept ","type":""},{"question":"know ","response":"know knew known savoir conna\u00eetre","type":""},{"question":"savoir conna\u00eetre","response":"know knew known","type":""},{"question":"lay","response":"lay laid laid poser ","type":""},{"question":"poser","response":"lay laid laid","type":""},{"question":"lead ","response":"lead led led mener","type":""},{"question":"mener ","response":"lead led led ","type":""},{"question":"learn ","response":"learn learnt learnt apprendre","type":""},{"question":"apprendre","response":"learn learnt learnt ","type":""},{"question":"leave","response":"leave left left quitter partir","type":""},{"question":"quitter partir","response":"leave left left","type":""},{"question":"lend ","response":"lend lent lent pr\u00eater","type":""},{"question":"pr\u00eater","response":"lend lent lent ","type":""},{"question":"let","response":"let let let laisser permettre","type":""},{"question":"laisser permettre","response":"let let let ","type":""},{"question":"lie","response":"lie lay lain \u00eatre allong\u00e9","type":""},{"question":"\u00eatre allong\u00e9","response":"lie lay lain","type":""},{"question":"light","response":"light lit lit allumer \u00e9clairer","type":""},{"question":"allumer \u00e9clairer","response":"light lit lit","type":""},{"question":"lose","response":"lose lost lost perdre","type":""},{"question":"perdre","response":"lose lost lost","type":""}]},{"title":"Anglais-verbes irr\u00e9guliers (M\/P)","id":"1357588920083","testItemVOs":[{"question":"make","response":"make made made faire fabriquer","type":""},{"question":"faire fabriquer","response":"make made made","type":""},{"question":"mean ","response":"mean meant meant signifier vouloir dire","type":""},{"question":"signifier vouloir dire","response":"mean meant meant","type":""},{"question":"meet","response":"meet met met rencontrer","type":""},{"question":"rencontrer","response":"meet met met","type":""},{"question":"pay","response":"pay paid paid payer","type":""},{"question":"payer","response":"pay paid paid ","type":""},{"question":"put","response":"put put put poser mettre","type":""},{"question":"poser mettre","response":"put put put ","type":""}]},{"title":"Espa\u00f1ol p.44","id":"1357672908353","testItemVOs":[{"question":"feo\/a","response":"laid\/e","type":""},{"question":"laid\/e","response":"feo\/a","type":""},{"question":"guapo\/a","response":"beau belle","type":""},{"question":"beau belle","response":"guapo\/a","type":""},{"question":"gordo\/a","response":"gros grosse","type":""},{"question":"gros grosse","response":"gordo\/a","type":""},{"question":"delgado\/a","response":"mince","type":""},{"question":"mince","response":"delgado\/a","type":""},{"question":"rizado\/a","response":"fris\u00e9\/e","type":""},{"question":"fris\u00e9\/e","response":"rizado\/a","type":""},{"question":"la piel","response":"la peau","type":""},{"question":"la peau","response":"la piel","type":""}]},{"title":"Espagnol-les pi\u00e8ces de la maison","id":"1357845085613","testItemVOs":[{"question":"la cocina","response":"la cuisine","type":""},{"question":"la cuisine","response":"la cocina","type":""},{"question":"el comedor","response":"la salle \u00e0 manger","type":""},{"question":"la salle \u00e0 manger","response":"el comedor","type":""},{"question":"el cuarto de bano","response":"la salle de bain","type":""},{"question":"la salle de bain","response":"el cuarto de bano","type":""},{"question":"el dormitorio el cuarto","response":"la chambre","type":""},{"question":"la chambre","response":"el dormitorio el cuarto","type":""},{"question":"el salo'n","response":"le salon","type":""},{"question":"le salon","response":"el salo'n","type":""},{"question":"la planta baja","response":"le rez de chauss\u00e9","type":""},{"question":"le rez de chauss\u00e9","response":"la planta baja","type":""},{"question":"la primera planta","response":"le premier \u00e9tage","type":""},{"question":"le premier \u00e9tage","response":"la primera planta","type":""},{"question":"la buhardilla","response":"les combles","type":""},{"question":"les combles","response":"la buhardilla","type":""}]},{"title":"Latin, vocabulaire pour le 16\/01","id":"1358067152787","testItemVOs":[{"question":"quia quod","response":"parce que","type":""},{"question":"parce que","response":"quia quod","type":""},{"question":"potestas","response":"potestas potestatis f le pouvoir","type":""},{"question":"le pouvoir","response":"potestas potestatis f","type":""},{"question":"praebeo","response":"praebeo es ere praebui praebitum offrir","type":""},{"question":"offrir","response":"praebeo es ere praebui praebitum","type":""},{"question":"tum tunc","response":"alors","type":""},{"question":"alors","response":"tum tunc","type":""},{"question":"nihil","response":"rien","type":""},{"question":"rien","response":"nihil","type":""},{"question":"cupio","response":"cupio is ere cupivi cupitum d\u00e9sirer","type":""},{"question":"d\u00e9sirer","response":"cupio is ere cupivi cupitum","type":""},{"question":"sed at","response":"mais","type":""},{"question":"mais","response":"sed at","type":""},{"question":"dolor","response":"dolor doloris m la douleur","type":""},{"question":"la douleur","response":"dolor doloris m","type":""},{"question":"interficio","response":"interficio is ere -feci -fectum tuer","type":""},{"question":"tuer","response":"interficio is ere -feci -fectum","type":""},{"question":"incipio","response":"incipio is ere coepi coeptum commencer","type":""},{"question":"commencer","response":"incipio is ere coepi coeptum","type":""}]},{"title":"Espagnol p.45","id":"1358103596988","testItemVOs":[{"question":"superhinchado","response":"super gonfl\u00e9","type":""},{"question":"super gonfl\u00e9","response":"superhinchado","type":""},{"question":"indomable","response":"indomptable","type":""},{"question":"indomptable","response":"indomable","type":""},{"question":"ho'rrido","response":"horrible","type":""},{"question":"horrible","response":"ho'rrido","type":""},{"question":"chata","response":"petit ","type":""},{"question":"petit","response":"chata","type":""},{"question":"en effecto","response":"en effet","type":""},{"question":"en effet","response":"en effecto","type":""}]},{"title":"Espagnol-visage","id":"1358103845775","testItemVOs":[{"question":"les sourcils","response":"las cejas","type":""},{"question":"las cejas","response":"les sourcils","type":""},{"question":"les t\u00e2ches de rousseur ","response":"las pecas","type":""},{"question":"las pecas ","response":"les t\u00e2ches de rousseur","type":""},{"question":"les oreilles ","response":"las orejas","type":""},{"question":"las orejas","response":"les oreilles","type":""},{"question":"les yeux","response":"los ojos","type":""},{"question":"los ojos ","response":"les yeux","type":""},{"question":"les cheveux","response":"el pelo","type":""},{"question":"el pelo","response":"les cheveux","type":""},{"question":"les cils","response":"las pestan*as","type":""},{"question":"las pestan*as","response":"les cils","type":""},{"question":"le nez","response":"la nariz","type":""},{"question":"la nariz ","response":"le nez","type":""},{"question":"la bouche","response":"la boca","type":""},{"question":"la boca","response":"la bouche","type":""},{"question":"les dents","response":"los dientes","type":""},{"question":"los dientes","response":"les dents","type":""},{"question":"les l\u00e8vres","response":"los labios","type":""}]},{"title":"Espagnol divers","id":"1358184650740","testItemVOs":[{"question":"la ventaja","response":"l'avantage","type":""},{"question":"l'avantage","response":"la ventaja","type":""},{"question":"el inconveniente ","response":"l\u2019inconv\u00e9nient ","type":""},{"question":"l'inconv\u00e9nient ","response":"el inconveniente","type":""},{"question":"la envidia","response":"elle l'envie","type":""},{"question":"elle l'envie","response":"la envidia","type":""},{"question":"tupido","response":"\u00e9pais","type":""},{"question":"\u00e9pais","response":"tupido","type":""},{"question":"sedoso","response":"soyeux","type":""},{"question":"soyeux","response":"sedoso","type":""},{"question":"la melena","response":"la chevelure","type":""},{"question":"la chevelure","response":"la melena","type":""},{"question":"un mon*o","response":"un chignon","type":""},{"question":"un chignon","response":"un mon*o","type":""},{"question":"respingono","response":"retrouss\u00e9","type":""},{"question":"retrouss\u00e9","response":"respingono","type":""},{"question":"ensortijado","response":"boucl\u00e9","type":""},{"question":"boucl\u00e9","response":"ensortijado ","type":""},{"question":"castan*o","response":"ch\u00e2tain","type":""},{"question":"ch\u00e2tain","response":"castan*o","type":""},{"question":"moreno","response":"brun","type":""},{"question":"brun","response":"moreno","type":""},{"question":"rubio","response":"blond","type":""},{"question":"blond","response":"rubio","type":""},{"question":"pelirrojo","response":"roux","type":""},{"question":"roux","response":"pelirrojo","type":""},{"question":"aceitunado","response":"oliv\u00e2tre","type":""},{"question":"oliv\u00e2tre","response":"aceitunado","type":""},{"question":"suave","response":"doux","type":""},{"question":"doux","response":"suave","type":""},{"question":"cola de caballo","response":"queue de cheval","type":""},{"question":"queue de cheval","response":"cola de caballo","type":""},{"question":"carnoso","response":"charnu","type":""},{"question":"charnu ","response":"carnoso","type":""},{"question":"engordar","response":"grossir","type":""},{"question":"grossir","response":"engordar","type":""},{"question":"astuto","response":"malin","type":""},{"question":"malin","response":"astuto","type":""},{"question":"sobre todo","response":"surtout","type":""},{"question":"surtout","response":"sobre todo","type":""},{"question":"nunca","response":"jamais","type":""},{"question":"jamais","response":"nunca","type":""}]},{"title":"Anglais-verbes irr\u00e9guliers (R\/S)","id":"1358186364243","testItemVOs":[{"question":"read ","response":"read read read lire","type":""},{"question":"lire","response":"read read read ","type":""},{"question":"ride","response":"ride rode ridden faire du cheval","type":""},{"question":"faire du cheval","response":"ride rode ridden","type":""},{"question":"ring ","response":"ring rang rung sonner","type":""},{"question":"sonner","response":"ring rang rung","type":""},{"question":"rise","response":"rise rose risen s'\u00e9lever se lever","type":""},{"question":"s'\u00e9lever se lever","response":"rise rose risen","type":""},{"question":"run ","response":"run ran run courir ","type":""},{"question":"courir","response":"run ran run","type":""},{"question":"say ","response":"say said said dire","type":""},{"question":"see","response":"see saw seen voir","type":""},{"question":"voir","response":"see saw seen","type":""},{"question":"sell ","response":"sell sold sold vendre","type":""},{"question":"vendre","response":"sell sold sold","type":""},{"question":"send","response":"send sent sent envoyer","type":""},{"question":"envoyer","response":"send sent sent ","type":""},{"question":"set","response":"set set set poser fixer mettre","type":""},{"question":"poser fixer mettre","response":"set set set","type":""},{"question":"shake","response":"shake shook shaken secouer","type":""},{"question":"secouer","response":"shake shook shaken","type":""},{"question":"shine","response":"shine shone shone briller","type":""},{"question":"briller","response":"shine shone shone","type":""},{"question":"shoot ","response":"shoot shot shot tirer","type":""},{"question":"tirer","response":"shoot shot shot","type":""},{"question":"show","response":"show showed shown montrer","type":""},{"question":"montrer","response":"show showed shown","type":""},{"question":"shut ","response":"shut shut shut fermer","type":""},{"question":"fermer","response":"shut shut shut","type":""},{"question":"sing ","response":"sing sang sung chanter","type":""},{"question":"chanter ","response":"sing sang sung","type":""},{"question":"sit ","response":"sit sat sat \u00eatre assis","type":""},{"question":"\u00eatre assis","response":"sit sat sat","type":""}]},{"title":"Espagnol adjectifs (1)","id":"1358345131296","testItemVOs":[{"question":"tupido","response":"\u00e9pais","type":""},{"question":"\u00e9pais","response":"tupido","type":""},{"question":"guapo","response":"beau","type":""},{"question":"beau","response":"guapo","type":""},{"question":"astuto","response":"malin","type":""},{"question":"malin","response":"astuto","type":""},{"question":"superhinchado","response":"super gonfl\u00e9","type":""},{"question":"super gonfl\u00e9","response":"superhinchado","type":""},{"question":"aceitunado","response":"oliv\u00e2tre","type":""},{"question":"oliv\u00e2tre","response":"aceitunado","type":""}]},{"title":"Anglais-verbes irr\u00e9guliers (S\/suite)","id":"1358796211752","testItemVOs":[{"question":"sleep","response":"sleep slept slept dormir","type":""},{"question":"dormir","response":"sleep slept slept","type":""},{"question":"smell","response":"smell smelt smelt sentir ","type":""},{"question":"sentir ","response":"smell smelt smelt","type":""},{"question":"speak","response":"speak spoke spoken parler","type":""},{"question":"parler","response":"speak spoke spoken","type":""},{"question":"spell","response":"spell spelt spelt \u00e9peler","type":""},{"question":"\u00e9peler","response":"spell spelt spelt","type":""},{"question":"spend","response":"spend spent spent passer d\u00e9penser","type":""},{"question":"passer d\u00e9penser","response":"spend spent spent","type":""},{"question":"spoil","response":"spoil spoilt spoilt g\u00e2ter","type":""},{"question":"g\u00e2ter","response":"spoil spoilt spoilt","type":""},{"question":"spread","response":"spread spread spread \u00e9taler","type":""},{"question":"\u00e9taler","response":"spread spread spread","type":""},{"question":"stand","response":"stand stood stood \u00eatre debout","type":""},{"question":"\u00eatre debout","response":"stand stood stood","type":""},{"question":"steal","response":"steal stole stolen voler","type":""},{"question":"voler","response":"steal stole stolen","type":""},{"question":"stick","response":"stick stuck stuck coller","type":""},{"question":"coller","response":"stick stuck stuck","type":""},{"question":"sweep","response":"sweep swept swept balayer","type":""},{"question":"balayer","response":"sweep swept swept","type":""},{"question":"swim","response":"swim swam swum nager","type":""},{"question":"nager","response":"swim swam swum","type":""}]},{"title":"Espagnol-v\u00eatements","id":"1358922705114","testItemVOs":[{"question":"el traje","response":"le costume","type":""},{"question":"le costume","response":"el traje","type":""},{"question":"la camisa","response":"la chemise","type":""},{"question":"la chemise","response":"la camisa","type":""},{"question":"la co'rbata","response":"la cravatte","type":""},{"question":"la cravatte","response":"la co'rbata","type":""},{"question":"llevar","response":"porter","type":""},{"question":"porter","response":"llevar","type":""}]},{"title":"Espagnol-BD","id":"1358922880297","testItemVOs":[{"question":"el co'mic","response":"el co'mic el tebeo la historia la bd","type":""},{"question":"la bd","response":"el co'mic el tebeo la historia","type":""},{"question":"la tira","response":"la bande","type":""},{"question":"la bande","response":"la tira","type":""},{"question":"la vin*eta","response":"la vignette","type":""},{"question":"la vignette","response":"la vin*eta","type":""},{"question":"el globo","response":"la bulle","type":""},{"question":"la bulle","response":"el globo","type":""},{"question":"el dibujante","response":"le dessinateur","type":""},{"question":"le dessinateur","response":"el dibujante","type":""},{"question":"dibujar","response":"dessiner","type":""},{"question":"dessiner","response":"dibujar","type":""}]},{"title":"Alemand-","id":"1359139648668","testItemVOs":[]},{"title":"Anglais-verbes irr\u00e9guliers (T\/U)","id":"1359212350896","testItemVOs":[{"question":"take","response":"take took taken prendre","type":""},{"question":"prendre","response":"take took taken","type":""},{"question":"teach","response":"teach taught taught enseigner","type":""},{"question":"enseigner","response":"teach taught taught","type":""},{"question":"tear","response":"tear tore torn d\u00e9chirer","type":""},{"question":"d\u00e9chirer","response":"tear tore torn","type":""},{"question":"tell","response":"tell told told dire raconter","type":""},{"question":"dire raconter","response":"tell told told","type":""},{"question":"think","response":"think thought thought penser","type":""},{"question":"penser","response":"think thought thought","type":""},{"question":"throw","response":"throw threw thrown jeter","type":""},{"question":"jeter","response":"throw threw thrown","type":""},{"question":"understand","response":"understand understood understood comprendre","type":""},{"question":"comprendre","response":"understand understood understood","type":""}]}]"""
#aglae="""[{"title":"Anglais","id":"1350835092409","testItemVOs":[{"question":"maison","response":"home","type":""},{"question":"voiture","response":"car","type":""},{"question":"moi m\u00eame","response":"myself","type":""},{"question":"un enfant","response":"a child","type":""},{"question":"des enfants","response":"children","type":""},{"question":"ordinateur","response":"computer","type":""}]},{"title":"Latin","id":"1352830819064","testItemVOs":[{"question":"une d\u00e9esse","response":"dea, ae, f","type":""},{"question":"une lettre","response":"epistula, ae, f","type":""},{"question":"la for\u00eat","response":"silva, ae, f","type":""},{"question":"l'eau","response":"aqua, ae, f","type":""},{"question":"une jeune fille","response":"puella, ae, f","type":""},{"question":"une maison","response":"villa, ae, f","type":""},{"question":"une route","response":"via, ae, f","type":""},{"question":"une fille","response":"filia, ae, f","type":""},{"question":"la vie","response":"vita, ae, f","type":""},{"question":"un po\u00e8te","response":"poeta, ae, m","type":""}]},{"title":"Latin - Hercules","id":"1352831036764","testItemVOs":[{"question":"p\u00e8re et m\u00e8re","response":"Zeus \/ Jupiter et Alcm\u00e8ne une mortelle","type":""},{"question":"qu'a fait Hercules et \u00e0 quoi est-il condamn\u00e9","response":"tua ses 3 enfants, oracle \u00e0 Delphes, se mettre au service d'Eurysth\u00e9e","type":""},{"question":"N\u00e9m\u00e9e","response":"Lion","type":""},{"question":"Lerne","response":"Hydre, 8\/9 t\u00eates, sang empoisonn\u00e9","type":""},{"question":"biche","response":"de C\u00e9rynie qu'il poursuit une ann\u00e9e","type":""},{"question":"sanglier","response":"d'Erymanthe, effrayant","type":""},{"question":"cerb\u00e8re","response":"chien qui garde la porte des enfers","type":""},{"question":"pommes","response":"pommes d'or du jardin des Hep\u00e9rides","type":""},{"question":"\u00e9curies","response":"d'Augias, d\u00e9tourne 2 fleuves","type":""},{"question":"ceinture","response":"de la reine des Amazones","type":""},{"question":"boeufs","response":"de G\u00e9ryon qu'Hercules doit aller chercher au bout du monde","type":""},{"question":"les juments","response":"de Diom\u00e8de","type":""},{"question":"le taureau","response":"de Cr\u00eate, donn\u00e9 par Pos\u00e9idon \u00e0 Minos, le roi de Cr\u00eate","type":""}]},{"title":"Latin 2","id":"1355853352966","testItemVOs":[{"question":"video","response":"es ere voir","type":""},{"question":"audio","response":"is ire ecouter entendre","type":""},{"question":"capio","response":"is ire prendre","type":""},{"question":"mitto ","response":"is ere envoyer","type":""},{"question":"amo","response":"as are aimer","type":""},{"question":"do","response":"as are donner","type":""},{"question":"video","response":"es ere voir","type":""},{"question":"timeo","response":"es ere craindre","type":""},{"question":"colo","response":"is ere honorer cultiver","type":""},{"question":"duco","response":"is ere conduire","type":""}]},{"title":"latin 2 bis","id":"1355859535408","testItemVOs":[{"question":"aimer","response":"amo as are ","type":""},{"question":"donner","response":"do as are ","type":""},{"question":"conduire","response":"duco is ere ","type":""},{"question":"voir","response":"video es ere ","type":""},{"question":"craindre ","response":"timeo es ere ","type":""},{"question":"honorer cultiver","response":"colo is ere ","type":""},{"question":"envoyer","response":"mitto is ere ","type":""},{"question":"entendre ecouter","response":"audio is ire","type":""},{"question":"venir","response":"venio is ire ","type":""},{"question":"prendre ","response":"capio is ere","type":""}]},{"title":"m\u00e9tamorphoses latin","id":"1358438153652","testItemVOs":[{"question":"pour s\u00e9duire alcmene il se transforme en :               et prend l'apparence du serviteur :","response":"amphitrion sosie","type":""},{"question":"pour s\u00e9duire leda il se transforme en :","response":"cygne","type":""},{"question":"pour seduire dana\u00e9 enferm\u00e9 dans une tour il prend l'apparence de :","response":"d'une pluie d'or","type":""},{"question":"pour seduire europe il se transforme en :","response":"taureau blanc ","type":""},{"question":"narcisse :","response":"il est tomb\u00e9 amoureux de son propre reflet . en se voyant dans un lac , il se penche pour se voir et  meurt. les dieux ayants piti\u00e9 le transforment en narcisse , d'ou sa position pench\u00e9e vers l'eau. ","type":""},{"question":"la nymphe echo:","response":"elle est trop bavarde ; hera la condamne a devoir repeter sans cesse les dernieres paroles de ses interlocuteurs . c'est de la que vient l'echo des montagnes .","type":""},{"question":"arachn\u00e9 :","response":"elle est tres fier de ses talents de brodeuse , et elle defi hera qui la transforme alors en araign\u00e9 ","type":""},{"question":"circ\u00e9 :","response":"elle transforme les compagnons d'ulysse en porc quand ils arrivent chez elle ","type":""},{"question":"le rois midas :","response":"il n'a pas su reconnaitre la musique divine d'apollon de celle de pan , alors celui ci lui fais pousser des oreilles d'ane ","type":""},{"question":"argus :","response":"hera le remerci en mettant tous ses yeux sur la queu de son animal pr\u00e9f\u00e9rer ","type":""},{"question":"daphn\u00e9e:","response":"pour echaper a la folie amoureuse d'apollon , elle va etre transform\u00e9 par son pere en laurier ","type":""},{"question":"toutes ces histoires son consign\u00e9es dans et par  :","response":"par ovide dans un ouvrage intitul\u00e9 les m\u00e9tamorphoses ","type":""}]},{"title":"conjugaison au pr\u00e9sent  latin","id":"1358439122009","testItemVOs":[{"question":"o as are ","response":"o as at amus atis ant ","type":""},{"question":"eo es ere ","response":"eo es et emus estis ent ","type":""},{"question":"o is ire ","response":"o is it imus itis unt ","type":""},{"question":"io is ire       io is ere ","response":"io is it imus itis iunt ","type":""}]},{"title":"histoire ","id":"1358701710645","testItemVOs":[{"question":"pourquoi ces chevalier combattent il ? ou combattent ils ?","response":"a l'appel du pape des chevaliers chretiens viennent defendre les byzanthin contre les turcs et les arabes musulmans .ils partent pour des raisons religieuses et pour conquerir des terres . la premiere croisade (1096 1099) va les mener jusqu'a jerusaleme . la ville est pill\u00e9e et les habtant massacr\u00e9s. apres avoir pris la ville ils cr\u00e9s les etats latins. des regions deviennent aussi catholiques au nord et au sud de l'europe.","type":""},{"question":"quels sont les marchandises echang\u00e9es ? d'ou viennent elles ? ou vont elles ?","response":"a partir du 11 eme siecles , le commerce lointin se developpe .on echange differentes marchandises , mais surtout des epice et du tissu. les produits circulent entre l'orient et le nord de l'europe en passant par des villes comme venise ou bruge.les echanges sont nombreux dans des foires comme celle de champagne.","type":""},{"question":"comment un commercant a t il pu devenir noble ?","response":"jacque coeur est un marchand de la ville de bourge. l'installation du roi et de sa cour dans la ville au 15 eme siecle lui a parmit de s'enrichir et de developper ses activit\u00e9es.en plus du commerce il devient banquier et prete de l'argent au roi et aux nobles. ilexploitait aussi des mines et possedait des seigneuries. il devint conseill\u00e9 du roi qui le fit devenir noble.","type":""}]}]"""

if __name__ == "__main__":
    run_wsgi_app(application)
    
