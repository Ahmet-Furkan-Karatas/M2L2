import aiohttp
import random
from datetime import datetime, timedelta

# Datetime nesnesini oluşturma
now = datetime.now()

# Geçerli saat ve tarih çıktısı
print("Geçerli saat ve tarih:", now)

class Pokemon:
    pokemons = {}

    def __init__(self, pokemon_trainer):
        self.pokemon_trainer = pokemon_trainer
        self.pokemon_number = random.randint(1, 1000)
        self.img = None
        self.name = None
        self.hp = random.randint(1,100)
        self.power = random.randint(1,100)
        self.last_feed_time=datetime.now
        self.attack = "Atak"
        self.feed = "besle"
    
    async def attack(self, enemy):
        if isinstance(enemy, Wizard):  # Enemy'nin bir Wizard veri tipi olduğunu (Büyücü sınıfının bir örneği olduğunu) kontrol etme
            şans = random.randint(1, 5) 
            if şans == 1:
                return "Sihirbaz Pokémon, savaşta bir kalkan kullanıldı!"
            if enemy.hp > self.power:
                enemy.hp -= self.power
                return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ne saldırdı\n@{enemy.pokemon_trainer}'nin sağlık durumu{enemy.hp}"
            else:
                enemy.hp = 0
                return f"Pokémon eğitmeni @{self.pokemon_trainer} @{enemy.pokemon_trainer}'ni yendi!"

    async def get_name(self):
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data['forms'][0]['name']
                else:
                    return "Pikachu"

    async def info(self):
        if not self.name:
            self.name = await self.get_name()
        return f"Pokémonunuzun ismi: {self.name} \n Pokemonunuzun sağlığı: {self.hp} \n Pokemonunuzun gücü: {self.power}"   

    async def show_img(self):
        # PokeAPI aracılığıyla bir Pokémon'un adını almak için eşzamansız bir yöntem
        url = f'https://pokeapi.co/api/v2/pokemon/{self.pokemon_number}'
        async with aiohttp.ClientSession() as session:  # Bir HTTP oturumu açmak
            async with session.get(url) as response:  # Pokémon verilerini almak için bir GET isteği gönderme
                if response.status == 200:
                    data = await response.json()  # JSON yanıtının alınması
                    img_url = data['sprites']['front_default']  # Bir Pokémonun URL'sini alma
                    return img_url  # Resmin URL'sini döndürme
                else:
                    return None  # İstek başarısız olursa None döndürür

    async def feed(self, feed_interval=20, hp_increase=10):
        current_time = datetime.now()
        delta_time = timedelta(seconds=feed_interval)
        if (current_time - self.last_feed_time) > delta_time:
            self.hp += hp_increase
            self.last_feed_time = current_time
            return f"Pokémon'un sağlığı geri yüklenir. Mevcut sağlık: {self.hp}"
        else:
            return f"Pokémonunuzu şu zaman besleyebilirsiniz: {current_time+delta_time}"
        
class Wizard (Pokemon):    
    async def attack(self, enemy):
        return await super().attack(enemy)

    async def feed(self):
        return super().feed(feed_interval=15)

class Fighter (Pokemon):                        
    async def attack(self, enemy):
        süper_güç = random.randint(5, 15)  
        self.güç += süper_güç
        sonuç = await super().attack(enemy)  
        self.güç -= süper_güç
        return sonuç + f"\nDövüşçü Pokémon süper saldırı kullandı. Eklenen güç: {süper_güç}"
    
    async def feed(self):
        return super().feed(hp_increase=20)