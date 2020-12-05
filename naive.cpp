#include <bits/stdc++.h>
using namespace std;
#define MAX 5000


int n,s;
class Cirurgia{
public:
	int id,pri, w,e,ch,tc;
	int sala = -1,tc_inicio,tc_fim, dia;
	int semana,cirurgiao;
	Cirurgia(int id,int a,int b,int c,int d,int e){
		this->pri = a;
		this->w = b;
		this->e = c;
		this->ch = d;
		this->tc = e;
		this->id = id;
	}

	bool operator ==( Cirurgia const &b){
		return this->id == b.id;
	}

	bool operator < ( Cirurgia const & b){
		if(this->pri < b.pri){
			return true;
		}
		else if(this->pri == b.pri){
			if(b.w < this->w){
				return true;
			}
			else{
				if(this->tc <= b.tc){
					return true;
				}
			}
		}
		return false;
	}

	void setSala(int s){
		this->sala = s;
	}
	void setDia(int dia){
		this->dia = dia;
	}
	void setSemana(int sem){
		this->semana = sem;
	}
	void tempo(int a,int b){
		this->tc_inicio = a;
		this->tc_fim = b;
	}
	void setCirurgiao(int x){
		this->cirurgiao = x;
	}
};

class Cirurgiao{
public:
	int periodos_semanais;
	int periodos_dia;
	int especialidade;
	int periodo_ocupado;
	int id;
	Cirurgiao(int id, int tc , int ocupado , int e){
		this->id = id;
		this->periodos_semanais = tc;
		this->periodos_dia = tc;
		this->periodo_ocupado = ocupado;
		this->especialidade = e;

	}
	void addDiaria( int tc, int ocupado ){
		int periodo_ocupado = ocupado;
		periodos_dia += tc;
		periodos_semanais += tc;
	}
	void novaSemana(){
		periodos_semanais = 0;
		periodos_dia = 0;
	}

};

class Sala {
public:
	int id, disponivel;

	Sala(int id){
		this->id = id;
		this->disponivel =0;
	}

	void setHora(int d){
		disponivel = d + 2;
	}
	void novaSemana(){
		disponivel = 0;
	}

	bool operator < ( Sala const&b){
		if(this->disponivel < b.disponivel)
			return true;
		return false;
	}

};

vector<Cirurgia> cirurgias;
vector<Cirurgiao> cirurgioes;
vector<Sala> salas;
int cirurgias_realizadas = 0;
int semana = 1,dia = 0;
void agenda(int time){

	sort(cirurgias.begin(),cirurgias.end() );
	for(int i = 0;i<s;i++){
		
		if(salas[i].disponivel == 46)
			continue;
		// verifica se tem sala disponível
		for (int ci = 0 ; ci < cirurgias.size(); ci++ ){ // esse for está errado
			if(cirurgias[ci].sala != -1){
				continue;
			}
			// possivel agendar naquela salas
			
			if( time > salas[i].disponivel && salas[i].disponivel + cirurgias[ci].tc <= 46 ){

				// Procura um cirurgiao para atender, caso nao exista, criar um novo cirurgiao
				int cirurgiao_selecionado = -1;
				for(int c = 0; c<cirurgioes.size();c++ ){
					if( cirurgioes[c].especialidade == cirurgias[ci].e  &&  cirurgioes[c].periodos_dia + cirurgias[ci].tc <= 24 && 
					 	cirurgioes[c].periodos_semanais + cirurgias[ci].tc <= 100 && cirurgioes[c].periodo_ocupado < time ){
						cirurgiao_selecionado = cirurgioes[c].id;
					}
				}

				// agenda a cirurgia com o cirurgiao e com a sala selecionada.
				if(cirurgiao_selecionado != -1){
					cirurgioes[ci].addDiaria((cirurgias[ci].tc),time+cirurgias[ci].tc );
				}
				// cria um cirurgiao para fazer aquela cirurgia.
				else
				{

					Cirurgiao novo_cirurgiao(cirurgioes.size(), cirurgias[ci].tc, cirurgias[ci].tc+time, cirurgias[ci].e   );
					cirurgioes.push_back(novo_cirurgiao);
					novo_cirurgiao.addDiaria((cirurgias[ci].tc),time+cirurgias[ci].tc );
					cirurgiao_selecionado = novo_cirurgiao.id;
				}

				salas[i].setHora( time + cirurgias[ci].tc -1 );
				
				cirurgias[ci].setSala(salas[i].id);
				cirurgias[ci].tempo( time, time+cirurgias[ci].tc -1 );
				cirurgias[ci].setSemana(semana);
				cirurgias[ci].setDia(dia);
				cirurgias[ci].setCirurgiao(cirurgiao_selecionado);
				cirurgias_realizadas++;
			}
		}
	}
}

void zeraDisponibilidade(){
	for (int i = 0;i<s;i++){
		salas[i].novaSemana();
	}
	for(int i = 0;i<cirurgioes.size();i++){
		cirurgioes[i].novaSemana();
	}
}

int main(){
	
	scanf("%d %d",&n,&s);
	for(int i = 0;i<s;i++){
		Sala s(i+1);
		salas.push_back(s);
	}


	for(int i = 0;i<n;i++){
		int a,b,c,d,e,f;
		scanf("%d %d %d %d %d %d",&a,&b,&c,&d,&e,&f);	
		
		Cirurgia ci(a,b,c,d,e,f);
		
		cirurgias.push_back(ci);
	}
	// tempo atual
	int TC = 1;
	// Enquanto ainda tem cirurgia para serem atendidas.
	while( cirurgias_realizadas <  cirurgias.size()){
		agenda(TC);
		TC += 1;
		if(TC == 46){
			zeraDisponibilidade();
			TC = 1;
			dia++;
		}
		if(dia == 5){
			dia = 0;
			semana++;
		}

	}


	for(int i = 0;i<cirurgias.size();i++){
		printf("Cirurgia:%d, prioridade:%d ,Agendada na semana:%d no dia: %d, nos horários: [%d %d], Na sala: %d pelo Cirurgião: %d\n\n\n"
			,cirurgias[i].id,cirurgias[i].pri, cirurgias[i].semana , cirurgias[i].dia ,cirurgias[i].tc_inicio,cirurgias[i].tc_fim,cirurgias[i].sala, cirurgias[i].cirurgiao);
	}

	return 0;
}