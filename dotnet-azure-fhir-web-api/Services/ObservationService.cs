using HDR_UK_Web_Application.IServices;
using Newtonsoft.Json.Linq;
using System.Collections.Generic;
using System.Threading.Tasks;
using System.IO;
using System.Diagnostics;

namespace HDR_UK_Web_Application.Services
{
    public class ObservationService : IObservationService
    {
        private static readonly string[] requestOption = new string[] {"/Observation/", "/Observation?patient=" };
        private readonly IResourceFetchService _resource;
        private readonly ILoggerManager _logger;

        public ObservationService(IResourceFetchService resource, ILoggerManager logger)
        {
            _resource = resource;
            _logger = logger;
        }

        public async Task<List<JObject>> GetPatientObservationPages(string id, int pages)
        {
            _logger.LogInfo("Class: ObservationService, Method: GetPatientObservationPages");
            return await _resource.GetPages($"{requestOption[1]}{id}", pages);
        }

        public async Task<JObject> GetSingleObservation(string id)
        {
            _logger.LogInfo("Class: ObservationService, Method: GetSingleObservation");
            JObject jObject = await _resource.GetSinglePage($"{requestOption[0]}{id}");

            Process process = new Process() 
            {
                StartInfo = new ProcessStartInfo{
                    FileName = "python3",
                    Arguments = "observation.py",
                    WorkingDirectory = Directory.GetCurrentDirectory(),
                    RedirectStandardInput = true
                }
            };

            process.Start();
            process.StandardInput.WriteLine(jObject.ToString());
            process.StandardInput.Close();

            return jObject;
        }

        public async Task<List<JObject>> GetPatientObservations(string id)
        {
            _logger.LogInfo("Class: ObservationService, Method: GetPatientObservations");
            return await _resource.GetAllPages($"{requestOption[1]}{id}");
        }
    }
}
