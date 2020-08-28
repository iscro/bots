using Mirai_CSharp;
using Mirai_CSharp.Models;
using Mirai_CSharp.Extensions;
using System;
using System.Drawing;
using System.Net;
using System.Runtime.CompilerServices;
using System.Threading.Tasks;
using Telegram.Bot;
using Telegram.Bot.Args;

/*                  Telegram QQ 消息互转
 *     使用了 https://github.com/Executor-Cheng/Mirai-CSharp
 *     和 https://github.com/TelegramBots/Telegram.Bot
 *     代码很乱而且没注释，赶工出来的，将就着看吧（
 */

namespace TGQQMsgExchange
{
    class Program
    {
        static ITelegramBotClient botClient;
        public static async Task Main(string[] args)
        {
            var Proxy = new WebProxy("127.0.0.1", 10809) { UseDefaultCredentials = true };
            botClient = new TelegramBotClient("xxxxxxxxxx:xx-xx-xx-xx", webProxy: Proxy);  //Telegram Bot Token

            var me = botClient.GetMeAsync().Result;
            botClient.OnMessage += Bot_OnTGMessage;
            botClient.StartReceiving();

            MiraiHttpSessionOptions options = new MiraiHttpSessionOptions("forwardmail", 8000, "***********");  //Mirai HTTP Api Token
            await using MiraiHttpSession session = new MiraiHttpSession();

            OnQQGroupMessage plugin1 = new OnQQGroupMessage();
            session.GroupMessageEvt += plugin1.GroupMessage;
            await session.ConnectAsync(options, 1919268092);
            Console.WriteLine("Started");
            Console.ReadLine();
            botClient.StopReceiving();

        }
        static async void Bot_OnTGMessage(object sender, MessageEventArgs e)
        {
            if (e.Message.Chat.Type == Telegram.Bot.Types.Enums.ChatType.Private)
            {
                await botClient.SendTextMessageAsync(
                  chatId: e.Message.Chat,
                  text: "私聊消息不会被转发"
                );
            }
            if (e.Message.Text != null && e.Message.Chat.Type == Telegram.Bot.Types.Enums.ChatType.Supergroup)
            {
                Console.WriteLine($"Received a Telegram text message in chat {e.Message.Chat.Id}.");
                MiraiHttpSessionOptions options = new MiraiHttpSessionOptions("forwardmail", 8000, "*********");  //Mirai HTTP Api Token
                await using MiraiHttpSession session = new MiraiHttpSession();
                await session.ConnectAsync(options, 1919268092);
                IMessageBase plain1 = new PlainMessage($"[Telegram]{e.Message.From.FirstName} {e.Message.From.LastName} : {e.Message.Text}");
                await session.SendGroupMessageAsync(808712612, plain1);
                await session.ReleaseAsync();

            }
        }




    }
    public partial class OnQQGroupMessage
    {
        static ITelegramBotClient botClient;
        public async Task<bool> GroupMessage(MiraiHttpSession session, IGroupMessageEventArgs e)
        {
            Console.WriteLine($"Received a QQ text message in chat {e.Sender.Group.Id}.");
            var Proxy = new WebProxy("127.0.0.1", 10809) { UseDefaultCredentials = true };
            botClient = new TelegramBotClient("1302965173:AAEkkZ7-G-cUnoDGrDt8-50fjxpTEUkQ6cI", webProxy: Proxy);
            var msg = string.Join("&&&&SPLIT&&&&", (System.Collections.Generic.IEnumerable<IMessageBase>)e.Chain);
            await botClient.SendTextMessageAsync(
                  chatId: -1001206672767,
                  text: $"[QQ]{e.Sender.Name} : {string.Join(null, msg.Split("&&&&SPLIT&&&&")[1])}",
                  disableNotification: true
                );

            return true;
        }
    }
}
